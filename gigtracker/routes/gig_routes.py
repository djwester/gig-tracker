from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from gigtracker.schema.base import get_session
from gigtracker.schema.gig import Gig, GigCreate, GigPublic

SessionDep = Annotated[Session, Depends(get_session)]
gig_router = APIRouter(prefix="/api")


@gig_router.post("/gigs", response_model=GigPublic, status_code=201)
def create_gig(gig: GigCreate, session: SessionDep):
    db_gig = Gig.model_validate(gig)

    session.add(db_gig)
    session.commit()
    session.refresh(db_gig)

    return db_gig


@gig_router.get("/gigs", response_model=list[GigPublic])
def get_gigs(session: SessionDep):
    gigs = session.exec(select(Gig)).all()

    return list(gigs)


@gig_router.put("/gigs/{gig_id}", response_model=GigPublic)
def update_gig(gig_id: int, gig: GigCreate, session: SessionDep):
    db_gig = session.get(Gig, gig_id)
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")

    gig_data = gig.model_dump(exclude_unset=True)
    db_gig.sqlmodel_update(gig_data)
    session.add(db_gig)
    session.commit()
    session.refresh(db_gig)

    return db_gig


@gig_router.delete("/gigs/{gig_id}", status_code=204)
def delete_gig(gig_id: int, session: SessionDep):
    gig = session.get(Gig, gig_id)
    if not gig:
        raise HTTPException(status_code=404, detail="Gig not found")

    session.delete(gig)
    session.commit()

    return Response(status_code=204)
