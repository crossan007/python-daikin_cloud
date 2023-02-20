from dotenv import load_dotenv
from daikin_cloud import DaikinCloud
from logger import logger
import time

logger.debug("Loading environment")
load_dotenv()

logger.debug("Initializing DaikinCloud")
d = DaikinCloud()

installation_ids = list(d.installations.keys())
iid = installation_ids[0]
installation = d.installations[iid]

device = installation.devices["Home"]
logger.debug(device)


time.sleep(2.4)

device.set_device_value("setpoint_air_heat", 72)

# d.set_device_value(installation, update_command)
