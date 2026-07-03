import logging
from pathlib import Path
from typing import BinaryIO
from uuid import uuid4
from aiofiles import open, os
from core import settings


class FileService:

    async def save_file_and_get_path(self, file_name: str, file: BinaryIO) -> Path: 
        unique_name = f"{uuid4().hex}_{file_name}"
        destination = settings.FILES_DIR / unique_name
        relative_url_path = f"/static/files/{unique_name}"
        async with open(destination, "wb") as buffer:
            while chunk := file.read(1024 * 1024):
                await buffer.write(chunk)
                
        return relative_url_path
    
    async def delete_file(self, file_path: str) -> Path: 
        clear_file_path = file_path.lstrip("/")
        destination = settings.BASE_DIR / clear_file_path
        
        await os.remove(destination)
        
        return destination