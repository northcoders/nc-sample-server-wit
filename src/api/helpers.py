"""Miscellaneous helper functions, classes and custom errors"""
import os
import sys
from typing import TypedDict
import logging


# Logging config
logger = logging.getLogger("App")

file_loc = "./logs/app.log"

log_levels = {
    "error": logging.ERROR,
    "warn": logging.WARN,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}

log_level = log_levels[os.environ.get("LOG_LEVEL", "debug")]

file_handler = logging.FileHandler(file_loc)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(log_level)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


# Errors


class ItemNotFoundException(Exception):
    """Encapsulates an error following null results"""

    def __init__(self, item_name: str, item_id: int = None) -> None:
        """Initialise with provided error message."""
        m1 = f"No instance of {item_name} was found in the database"
        m2 = f" with id {item_id}." if item_id else "."
        self.message = f"{m1}{m2}"
        super().__init__(self.message)
