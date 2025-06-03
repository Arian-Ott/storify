import os
from dotenv import load_dotenv
from api.utils.logging import logger
from api.db import Base, engine
from api.utils.logging import setup_logging


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
    logger.info("Startup tasks completed.")
