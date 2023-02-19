"""Module: """
from logger import logger
import socketio


class DaikinDevice:
    """Class for interacting with device"""

    mac: str
    icon: str
    name: str
    acs_mode: bool
    sio: socketio.Client

    def __init__(self, device_data: any, sio: socketio.Client) -> None:
        self.acs_mode = False
        self.name = device_data["name"]
        self.icon = device_data["icon"]
        self.mac = device_data["mac"]
        self.sio = sio
        logger.debug("Setup device %s - %s", self.name, self.mac)

    def set_device_value(self, prop: str, value: str):
        """Sets a device value using the installation socket"""

        update_command = {"mac": self.mac, "property": prop, "value": value}

        def callback_fun():
            logger.debug(
                "(%s) POST - %s : %s",
                update_command["mac"],
                update_command["property"],
                update_command["value"],
            )

        self.sio.emit("create-machine-event", update_command, callback=callback_fun)
