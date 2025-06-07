from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from fastapi import Request
html_router = APIRouter( tags=["html"])
templates = Jinja2Templates(directory="frontend/templates", auto_reload=True)

@html_router.get("/", response_class=HTMLResponse)
async def route_index(request:Request):
    """
    Render the index page.
    """
    return templates.TemplateResponse("index.html", {"request": request})