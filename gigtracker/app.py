from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.security import HTTPBasic
from fastapi.staticfiles import StaticFiles

from gigtracker.routes.gig_routes import gig_router
from gigtracker.routes.ui_routes import ui_router
from gigtracker.routes.user_routes import user_router
from gigtracker.schema.base import create_db_and_tables, drop_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    drop_db_and_tables()


app = FastAPI(lifespan=lifespan)
security = HTTPBasic()

app.include_router(ui_router)
app.include_router(gig_router)
app.include_router(user_router)

app.mount("/static", StaticFiles(directory="gigtracker/static"), name="static")
