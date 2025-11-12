# utils/logger.py

import logging
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_DIR / "app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def get_logger(name=__name__):
    """
    Returns a logger instance for the given module name
    """
    return logging.getLogger(name)
