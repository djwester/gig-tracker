from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from gigtracker.schema.base import get_session
from gigtracker.schema.gig import Gig

SessionDep = Annotated[Session, Depends(get_session)]
api_router = APIRouter(prefix="/api")


@api_router.post("/gigs", status_code=201)
def create_gig(gig: Gig, session: SessionDep) -> Gig:
    gig.date = datetime.fromisoformat(gig.date)
    session.add(gig)
    session.commit()
    session.refresh(gig)

    return gig


@api_router.get("/gigs", response_model=list[Gig])
def get_gigs(session: SessionDep) -> list[Gig]:
    gigs = session.exec(select(Gig)).all()

    return list(gigs)


@api_router.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig: Gig, session: SessionDep) -> Gig:
    db_gig = session.get(Gig, gig_id)
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")

    gig.date = datetime.fromisoformat(gig.date)

    gig_data = gig.model_dump(exclude_unset=True)
    db_gig.sqlmodel_update(gig_data)
    session.add(db_gig)
    session.commit()
    session.refresh(db_gig)

    return db_gig


@api_router.delete("/gigs/{gig_id}", status_code=204)
def delete_gig(gig_id: int, session: SessionDep):
    gig = session.get(Gig, gig_id)
    if not gig:
        raise HTTPException(status_code=404, detail="Gig not found")

    session.delete(gig)
    session.commit()

    return {"message": "Gig deleted"}
