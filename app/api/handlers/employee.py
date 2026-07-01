
import logging
from typing import Annotated, List
from fastapi import APIRouter, UploadFile, File, Depends, Form, Query
from pydantic import Json



logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/employees/")
async def create_employee(
    
):
    pass

@router.get("/employee/")
async def get_employee(
    
):
    return 

@router.put("/employee/{uuid}")
async def put_employee(
    
):
    return 

@router.delete("/employee/{uuid}")
async def delete_employee(
    
):
    return 