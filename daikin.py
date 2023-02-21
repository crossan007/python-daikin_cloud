"""test program"""
import asyncio
from dotenv import load_dotenv
from daikin_cloud import DaikinCloud
from logger import logger, log_to_console
import json


loop = asyncio.get_event_loop()


log_to_console()


async def main():
    """runner"""
    logger.debug("Loading environment")
    load_dotenv()
    logger.debug("Initializing DaikinCloud")
    d = DaikinCloud()
    await d.login_dev()
    logger.debug("profile %s", d.profile.email)


loop.create_task(main())
loop.run_forever()
