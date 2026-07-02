from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.config import settings
from app.api.routes import router as api_router
from core.logging_config import setup_logging

logger = setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
