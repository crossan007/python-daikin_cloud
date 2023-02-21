"""Logging module"""
import logging

logger = logging.getLogger("Daikin")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.NOTSET)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)

log_everything = False


def log_to_console():
    logger.addHandler(ch)
    logger.debug("Logger Initialized")


if log_everything:
    logging.basicConfig(level=logging.NOTSET)
