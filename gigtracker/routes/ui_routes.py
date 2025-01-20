from datetime import date, time
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from jinja2_fragments.fastapi import Jinja2Blocks
from sqlmodel import Session, select

from gigtracker.schema.base import get_session
from gigtracker.schema.gig import Gig
from gigtracker.schema.venue import Venue

ui_router = APIRouter()

templates = Jinja2Blocks(directory="gigtracker/templates")
SessionDep = Annotated[Session, Depends(get_session)]


@ui_router.get("/", include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@ui_router.get("/gigs", include_in_schema=False)
def gigs(request: Request, session: SessionDep):
    result = session.exec(select(Gig)).all()

    return templates.TemplateResponse("gigs.html", {"request": request, "gigs": result})


@ui_router.post("/gigs", include_in_schema=False)
def create_gig(
    request: Request,
    gig_date: Annotated[date, Form()],
    gig_name: Annotated[str, Form()],
    session=Depends(get_session),
):
    gig = Gig(
        date=gig_date,
        name=gig_name,
        time=time.fromisoformat("03:55"),
        venue_id=1,
        client_id=2,
    )
    session.add(gig)
    session.commit()

    return templates.TemplateResponse(
        "gigs.html",
        {"request": request, "gigs": [gig]},
    )


@ui_router.get("/load_venue_options", include_in_schema=False)
def get_venues_as_options(request: Request, session: SessionDep):
    venues = session.exec(select(Venue)).all()

    return templates.TemplateResponse(
        "snippets/venue_as_options.html", {"request": request, "venues": venues}
    )
