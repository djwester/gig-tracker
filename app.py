import solara.server.fastapi
from fastapi import FastAPI

app = FastAPI()


@app.get("/api")
async def root():
    return {"message": "Hello World"}


app.mount("/gigtracker/ui/", app=solara.server.fastapi.app)
