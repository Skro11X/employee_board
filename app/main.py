from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.config import settings
from api import api_router, web_router
from core.logging_config import setup_logging

logger = setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(web_router)
app.include_router(api_router)
