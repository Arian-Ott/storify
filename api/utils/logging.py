import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("api_logger")


def setup_logging(
    log_file="api.log", max_bytes=10 * 1024 * 1024, backup_count=5
):
    """
    Set up logging configuration for the API.

    Args:
        log_file (str): The name of the log file.
        max_bytes (int): Maximum size of the log file before rotation.
        backup_count (int): Number of backup files to keep.
    """
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count
    )
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.info("Logging setup complete.")
