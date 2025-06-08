import os
from dotenv import load_dotenv
from api.utils.logging import logger
from api.db import Base, engine
from api.utils.logging import setup_logging
from api.services.user_service import create_user, get_user
from api.schemas.user_schemas import UserCreate
import requests
def create_admin_user():
    if get_user(username="storify_admin"):
        logger.info("Admin user already exists. Skipping creation.")
        return
    admin_user = UserCreate(
        username="storify_admin",
        password="changeme_later",
    )
    create_user(admin_user)
    logger.info("Admin user created successfully.")

def download_latest_tailwind():
    js = requests.get(
        "https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"
    ).text
    if not os.path.exists("frontend/static/"):
        os.makedirs("frontend/static/")
        logger.info("Created directory for Tailwind CSS.")
    os.remove("frontend/static/tailwind.js")
    with open("frontend/static/tailwind.js", "w", encoding="utf-8") as f:
        f.write(js)

def create_tables():
    Base.metadata.create_all(bind=engine)


def create_storage_path():
    if not os.path.exists("storage"):
        try:
            os.makedirs("storage")
            logger.info("Storage directory created successfully.")
        except Exception as e:
            logger.error(f"Failed to create storage directory: {e}")


def load_environment_variables():
    """
    Load environment variables from a .env file.
    """
    if not os.path.exists(".env"):
        logger.warning(".env file not found. Ensure it exists in the project root.")

    load_dotenv(verbose=True)
    logger.info("Environment variables loaded from .env file.")


def startup():
    """
    Perform startup tasks such as loading environment variables.
    """
    setup_logging()
    create_storage_path()
    load_environment_variables()
    create_tables()
    create_admin_user()
    download_latest_tailwind()
    logger.info("Startup tasks completed.")
