from fastapi import APIRouter, HTTPException, UploadFile, File
from api.services.s4_service import create_file, get_file

s4_router = APIRouter(prefix="/s4")


# Example FastAPI endpoint for uploading and compressing a file
@s4_router.post("/upload/")
async def upload_file(file: UploadFile = File(...), compress: bool = False):
    file_bytes = await file.read()
    result = create_file(file.filename, file_bytes, file.content_type)
    return result


@s4_router.get("/s4_storage/{file_id}")
async def api_get_file(file_id: str):
    """
    Retrieve a file by its ID.
    """
    file_data = get_file(file_id)
    if file_data:
        return file_data
    raise HTTPException(status_code=501, detail="Not implemented yet")
