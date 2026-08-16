"""
JeevanGrid Logging Configuration Module
Configures structured console and file logging with standardized format.
"""

import logging
import sys
from typing import Optional
from backend.app.core.config import settings


def setup_logging(log_level: Optional[str] = None) -> logging.Logger:
    """Configures application-wide root logging."""
    level_str = log_level or settings.LOG_LEVEL
    numeric_level = getattr(logging, level_str.upper(), logging.INFO)

    log_format = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        datefmt=date_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    # Suppress overly verbose third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING if not settings.DEBUG else logging.INFO)
    logging.getLogger("passlib").setLevel(logging.WARNING)

    logger = logging.getLogger("jeevangrid")
    logger.setLevel(numeric_level)
    return logger


logger = setup_logging()
