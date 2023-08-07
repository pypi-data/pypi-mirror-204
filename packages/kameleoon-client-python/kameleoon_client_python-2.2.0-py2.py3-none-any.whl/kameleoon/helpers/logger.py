"""Logger"""

import logging


def get_logger() -> logging.Logger:
    """Return logging.Logger instance with custom settings"""
    handler = logging.StreamHandler()
    format_ = logging.Formatter(
        "%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
    )
    handler.setFormatter(format_)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
