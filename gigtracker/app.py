from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from gigtracker.routes.client_routes import client_router
from gigtracker.routes.gig_routes import gig_router
from gigtracker.routes.ui_routes import ui_router
from gigtracker.routes.user_routes import user_router
from gigtracker.schema.base import create_db_and_tables, drop_db_and_tables, get_session
from gigtracker.schema.security import Token
from gigtracker.schema.user import User
from gigtracker.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    drop_db_and_tables()


app = FastAPI(lifespan=lifespan)


SessionDep = Annotated[Session, Depends(get_session)]


@app.post("/token", response_model=Token)
def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not authenticate_user(user, form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    assert user  # for mypytype checking

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


app.include_router(ui_router)
app.include_router(gig_router)
app.include_router(user_router)
app.include_router(client_router)

app.mount("/static", StaticFiles(directory="gigtracker/static"), name="static")
