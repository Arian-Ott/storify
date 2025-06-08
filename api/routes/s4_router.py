from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from api.services.s4_service import create_file, get_file
from api.utils.jwt import protected_route
from api.routes.jwt import oauth2_bearer
from fastapi import Request
from fastapi import Form
from api.utils.jwt import verify_token
from fastapi.responses import RedirectResponse

s4_router = APIRouter(prefix="/s4")


@s4_router.post("/upload/")
@protected_route
async def upload_file(
    file: UploadFile = File(...), token: str = Depends(oauth2_bearer)
):
    file_bytes = await file.read()
    token = dict(verify_token(token))
    user_id = token.get("sub")
    result = create_file(file.filename, file_bytes, file.content_type, user_id=user_id)
    return result


@s4_router.get("/s4_storage/{file_id}")
async def api_get_file(
    file_id: str,
):
    """
    Retrieve a file by its ID.
    """
    file_data = get_file(file_id)
    if file_data:
        return file_data
    raise HTTPException(status_code=501, detail="Not implemented yet")


@s4_router.post("/s4_storage/multipart")
@protected_route
async def api_upload_file_multipart(
    request: Request,
    file: UploadFile,
    file_name: str = Form(...),
):
    """
    Upload a file using multipart form data.
    """
    file_bytes = await file.read()
    print(f"File bytes length: {len(file_bytes)}")

    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing access token")

    token = verify_token(token)
    user_id = token.get("sub")

    create_file(
        file_name,
        user_id,
        file_bytes,
        file.content_type,
    )
    return RedirectResponse(
        url="/assets",
        status_code=303,
    )
