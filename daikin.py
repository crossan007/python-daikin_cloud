import logging
from dotenv import load_dotenv
from daikin_cloud import DaikinCloud

load_dotenv()
logging.basicConfig(level="NOTSET")

d = DaikinCloud()

d.fetch_installations()

installation_ids = list(d.installations.keys())
iid = installation_ids[0]

installation = d.installations[iid]

device = installation.devices["Home"]

print(device)

# device.set_device_value("power", 0)

# d.set_device_value(installation, update_command)
