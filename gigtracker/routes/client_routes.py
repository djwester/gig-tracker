from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from gigtracker.schema.base import get_session
from gigtracker.security import verify_token

SessionDep = Annotated[Session, Depends(get_session)]
client_router = APIRouter(prefix="/api")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@client_router.get("/clients")
def get_clients(session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Clients"}
