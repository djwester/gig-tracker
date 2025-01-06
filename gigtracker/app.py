from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from gigtracker.routes.gig_routes import gig_router
from gigtracker.routes.ui_routes import ui_router
from gigtracker.routes.user_routes import user_router
from gigtracker.schema.base import create_db_and_tables, drop_db_and_tables, get_session
from gigtracker.schema.user import User
from gigtracker.security import authenticate_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    drop_db_and_tables()


app = FastAPI(lifespan=lifespan)
security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SessionDep = Annotated[Session, Depends(get_session)]


@app.post("/token")
def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not authenticate_user(user, form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"access_token": user.hashed_password, "token_type": "bearer"}  # type: ignore [union-attr]


app.include_router(ui_router)
app.include_router(gig_router)
app.include_router(user_router)

app.mount("/static", StaticFiles(directory="gigtracker/static"), name="static")
