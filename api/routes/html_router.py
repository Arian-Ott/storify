from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from api.utils.jwt import visitors
from fastapi.templating import Jinja2Templates
from fastapi import Request
from api.utils.jwt import verify_token
from api.routes.user import user_router
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import HTTPException
from api.utils.jwt import protected_route
from api.services.s4_service import get_symlinks_by_user

html_router = APIRouter(tags=["html"])
templates = Jinja2Templates(directory="frontend/templates", auto_reload=True)


def html_resp(request, html_file, data: dict = {}):
    logged_in = False
    access_token = request.cookies.get("access_token")
    try:
        verify_token(access_token)
        logged_in = True
    except Exception as e:
        logged_in = False

    return templates.TemplateResponse(
        html_file, {"request": request, "logged_in": logged_in, **data}
    )


@html_router.get("/", response_class=HTMLResponse)
@visitors(redirect_to="/dashboard")
async def route_index(request: Request):
    """
    Render the index page.
    """
    return html_resp(request, "index.html")


@html_router.get("/register", response_class=HTMLResponse)
@visitors(redirect_to="/dashboard")
async def route_register(request: Request):
    """
    Render the registration page.
    """
    return html_resp(request, "auth/register.html")


@html_router.get("/login", response_class=HTMLResponse)
@visitors(redirect_to="/dashboard")
async def route_login(request: Request):
    """
    Render the login page.
    """
    return html_resp(request, "auth/login.html")


@html_router.get("/sign-out")
@protected_route
async def route_sign_out(request: Request):
    """
    Sign out the user by deleting the JWT token cookie.
    """

    try:
        response = RedirectResponse(
            url="/",
            status_code=303,
        )
        response.delete_cookie("access_token")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}") from e


@html_router.get("/dashboard", response_class=HTMLResponse)
@protected_route
async def route_dashboard(request: Request):
    """
    Render the dashboard page.
    """

    username = verify_token(request.cookies.get("access_token")).get(
        "username", "Guest"
    )
    print(f"Dashboard accessed by user: {username}")
    return html_resp(request, "dashboard/dashboard.html", {"username": username})


@html_router.get("/storify", response_class=HTMLResponse)
@protected_route
async def route_storify(request: Request):
    """
    Render the Storify page.
    """
    return html_resp(request, "dashboard/storify.html")


@html_router.get("/assets", response_class=HTMLResponse)
@protected_route
async def route_assets(request: Request):
    """
    Render the Assets page.
    """
    files = get_symlinks_by_user(
        verify_token(request.cookies.get("access_token")).get("sub")
    )
    return html_resp(request, "dashboard/assets.html", {"files": files})
