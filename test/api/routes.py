import logging
from fastapi import APIRouter
from api.handlers.employee import router as employees_handlers

router = APIRouter(prefix="/api/v1")

router.include_router(employees_handlers, tags=["employees_handlers"]) 
