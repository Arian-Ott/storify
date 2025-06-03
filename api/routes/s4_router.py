from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from api.services.s4_service import create_file, get_file
from api.utils.jwt import protected_route
from api.routes.jwt import oauth2_bearer
from fastapi import Request
s4_router = APIRouter(prefix="/s4")



@s4_router.post("/upload/")
@protected_route
async def upload_file(file: UploadFile = File(...), token: str = Depends(oauth2_bearer)):

    file_bytes = await file.read()
    result = create_file(file.filename, file_bytes, file.content_type)
    return result


@s4_router.get("/s4_storage/{file_id}")
@protected_route
async def api_get_file( file_id: str, token: str = Depends(oauth2_bearer)):
    """
    Retrieve a file by its ID.
    """
    file_data = get_file(file_id)
    if file_data:
        return file_data
    raise HTTPException(status_code=501, detail="Not implemented yet")
