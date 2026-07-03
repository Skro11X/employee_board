from fastapi import APIRouter
from api.handlers.employee import api_router as employees_handlers_api
from api.handlers.employee import web_router as employees_handlers_web

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(employees_handlers_api, tags=["employees_api"]) 

web_router = APIRouter(prefix='', tags=["Web UI"])
web_router.include_router(employees_handlers_web, tags=["employees_web"])