from fastapi import FastAPI
from api.routes.user import user_router
from api.utils.startup import startup
from api.routes.jwt import jwt_router
from api.routes.s4_router import s4_router
from fastapi.staticfiles import StaticFiles
from api.routes.html_router import html_router
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

load_dotenv()
import os

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)
app.mount("/static", StaticFiles(directory="frontend/static/"), name="static")
app.add_event_handler("startup", startup)
app.include_router(user_router)
app.include_router(jwt_router)
app.include_router(s4_router)
from fastapi.staticfiles import StaticFiles


app.include_router(html_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

if __name__ == "__main__":
    import uvicorn

    load_dotenv()
    print("Starting the application...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
