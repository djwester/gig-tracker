from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from gigtracker.api_routes import api_router
from gigtracker.schema.base import create_db_and_tables
from gigtracker.ui_routes import ui_router

create_db_and_tables()

app = FastAPI()

app.include_router(ui_router)
app.include_router(api_router)

app.mount("/static", StaticFiles(directory="gigtracker/static"), name="static")
