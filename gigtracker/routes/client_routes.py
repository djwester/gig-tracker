from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from gigtracker.schema.base import get_session

SessionDep = Annotated[Session, Depends(get_session)]
client_router = APIRouter(prefix="/api")


@client_router.get("/clients")
def get_clients(session: SessionDep):
    return {"message": "Clients"}
