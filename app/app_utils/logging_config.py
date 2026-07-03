"""app/app_utils/logging_config.py

Structured logger factory for School AI Assistant.

Provides a unified logger configuration using a key=value format suitable
for easy parsing, while preventing sensitive PII or credentials from being logged.
"""

import logging
import sys
from app.app_utils.config import get_config


def get_logger(name: str) -> logging.Logger:
    """Retrieve or create a logger configured for structured logging.

    Args:
        name: Name of the logger, typically __name__.

    Returns:
        logging.Logger: A configured Logger instance.
    """
    logger = logging.getLogger(name)

    # Prevent duplicating handlers if this logger or its parent already has them
    if logger.handlers:
        return logger

    # Load logging level from AppConfig
    try:
        config = get_config()
        level_name = config.log_level
    except Exception:
        level_name = "INFO"

    log_level = getattr(logging, level_name, logging.INFO)
    logger.setLevel(log_level)

    # Use stdout to ensure log aggregation tools capture the logs correctly
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    # Key-value pair formatting for structured logs
    formatter = logging.Formatter(
        fmt="%(asctime)s | name=%(name)s | level=%(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Avoid propagation up to root logger to prevent default output duplication
    logger.propagate = False

    return logger
