from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from api.utils.jwt import visitors
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

@html_router.get("/register", response_class=HTMLResponse)
@visitors(redirect_to="/dashboard")
async def route_register(request: Request):
    """
    Render the registration page.
    """
    return templates.TemplateResponse("auth/register.html", {"request": request})