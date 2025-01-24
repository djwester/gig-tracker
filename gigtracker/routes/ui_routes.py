from datetime import date, time
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from jinja2_fragments.fastapi import Jinja2Blocks
from sqlmodel import Session, col, select

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


@ui_router.get("/venues", include_in_schema=False)
def venues(request: Request, session: SessionDep):
    result = session.exec(select(Venue)).all()

    return templates.TemplateResponse(
        "venue.html", {"request": request, "venues": result}
    )


@ui_router.post("/venues", include_in_schema=False)
def create_venue(
    request: Request,
    venue_name: Annotated[str, Form()],
    venue_address: Annotated[str, Form()],
    venue_city: Annotated[str, Form()],
    venue_contact_number: Annotated[str, Form()],
    venue_contact_email: Annotated[str, Form()],
    venue_capacity: int | None = Form(default=0),
    venue_notes: str = Form(default=None),
    session=Depends(get_session),
):
    if not venue_capacity:
        venue_capacity = None
    venue = Venue(
        name=venue_name,
        address=venue_address,
        city=venue_city,
        contact_number=venue_contact_number,
        contact_email=venue_contact_email,
        capacity=venue_capacity,
        notes=venue_notes,
    )
    session.add(venue)
    session.commit()

    return templates.TemplateResponse(
        "venue.html", {"request": request, "venues": [venue]}
    )


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
        "gigs.html", {"request": request, "gigs": [gig]}, block_name="content"
    )


@ui_router.get("/load_venue_options", include_in_schema=False)
def get_venues_as_options(request: Request, session: SessionDep):
    venues = session.exec(select(Venue)).all()

    return templates.TemplateResponse(
        "snippets/venue_as_options.html", {"request": request, "venues": venues}
    )


@ui_router.post("/search", include_in_schema=False)
def search(request: Request, session: SessionDep, search: Annotated[str, Form()]):
    # search_results = session.exec(select(Gig).where(Gig.name.like(f"%{search}%"))).all()
    search_results = session.exec(
        select(Gig).where(col(Gig.name).contains(search))
    ).all()
    return templates.TemplateResponse(
        "search.html", {"request": request, "search_results": search_results}
    )
