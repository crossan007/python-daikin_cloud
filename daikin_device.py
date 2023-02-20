"""Module: """
from logger import logger
import socketio
import json


class DaikinDevice:
    """Class for interacting with device"""

    mac: str
    icon: str
    name: str
    acs_mode: bool
    sio: socketio.Client
    sio_namespace: str

    def __init__(self, device_data: any, sio: socketio.Client, namespace: str) -> None:
        self.acs_mode = False
        self.name = device_data["name"]
        self.icon = device_data["icon"]
        self.mac = device_data["mac"]
        self.sio = sio
        self.sio_namespace = namespace
        logger.debug("Setup device %s - %s", self.name, self.mac)

    def set_device_value(self, prop: str, value: str):
        """Sets a device value using the installation socket"""

        update_command = {"mac": self.mac, "property": prop, "value": value}

        def callback_fun(data):
            logger.debug(
                "(%s) POST - %s : %s; (raw: %s)",
                update_command["mac"],
                update_command["property"],
                update_command["value"],
                json.dumps(data),
            )

        logger.debug("Setting device '%s' value '%s' to '%s'", self.mac, prop, value)

        self.sio.emit(
            "create-machine-event",
            update_command,
            callback=callback_fun,
            namespace=self.sio_namespace,
        )
