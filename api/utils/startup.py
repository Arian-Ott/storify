import os
from dotenv import load_dotenv
from api.utils.logging import logger


def load_environment_variables():
    """
    Load environment variables from a .env file.
    """

    env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    load_dotenv(env_path)
    logger.info("Environment variables loaded from .env file.")


def startup():
    """
    Perform startup tasks such as loading environment variables.
    """
    load_environment_variables()
    logger.info("Startup tasks completed.")
