from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

from app.api.routes import router
from app.api.frontend import router as frontend_router


app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

app.include_router(router)
app.include_router(frontend_router)