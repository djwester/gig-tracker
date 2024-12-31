from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from jinja2_fragments.fastapi import Jinja2Blocks
from sqlmodel import select

from gigtracker.schema.base import get_session
from gigtracker.schema.gig import Gig

ui_router = APIRouter()

templates = Jinja2Blocks(directory="gigtracker/templates")


@ui_router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@ui_router.get("/gigs")
def gigs(request: Request, session=Depends(get_session)):
    statement = select(Gig)
    result = session.exec(statement)

    return templates.TemplateResponse("gigs.html", {"request": request, "gig": result})


@ui_router.post("/gigs")
def create_gig(
    request: Request,
    gig_date: Annotated[date, Form()],
    gig_name: Annotated[str, Form()],
    session=Depends(get_session),
):
    gig = Gig(date=gig_date, venue=gig_name, location="Unknown")
    session.add(gig)
    session.commit()

    return templates.TemplateResponse(
        "gigs.html",
        {"request": request, "gigs": [gig]},
        block_name="test",
    )
    return templates.TemplateResponse("gigs.html", {"request": request, "gig": gig})
