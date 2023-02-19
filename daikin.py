from dotenv import load_dotenv
from daikin_cloud import DaikinCloud
from logger import logger

logger.debug("Loading environment")
load_dotenv()

exit()

logger.debug("Initializing DaikinCloud")
d = DaikinCloud()

installation_ids = list(d.installations.keys())
iid = installation_ids[0]
installation = d.installations[iid]


installation.connect_installation_socket()


device = installation.devices["Home"]
logger.debug(device)

# device.set_device_value("power", 0)

# d.set_device_value(installation, update_command)
