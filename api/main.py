from fastapi import FastAPI
from api.routes.user import user_router
from api.utils.startup import startup
from api.routes.jwt import jwt_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_event_handler("startup", startup)
app.include_router(user_router)
app.include_router(jwt_router)


if __name__ == "__main__":
    import uvicorn

    load_dotenv()
    print("Starting the application...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
