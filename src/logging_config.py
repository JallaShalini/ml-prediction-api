import logging
import os
from typing import Optional

from src.config import settings


def configure_logging() -> logging.Logger:
    log_level_name = (settings.log_level or os.getenv("LOG_LEVEL", "INFO")).upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger("ml_prediction_api")
    logger.setLevel(log_level)
    return logger


logger = configure_logging()
