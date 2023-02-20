"""Logging module"""
import logging

logger = logging.getLogger("Daikin")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.NOTSET)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug("Logger Initialized")

if False:
    logging.basicConfig(level=logging.NOTSET)
