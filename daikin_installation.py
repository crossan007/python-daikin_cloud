"""Module: """
import json
from logger import logger
import socketio
from daikin_device import DaikinDevice

class DaikinInstallation:
    """Class for interacting with an installation"""

    sio: socketio.Client
    api: any
    installation_id: str
    devices: dict[str, DaikinDevice]

    def __init__(self, api, installation_data) -> None:
        """Sets up this installation"""
        self.api = api
        self.devices = []
        self.installation_id = installation_data["_id"]
        self.devices: dict[str, DaikinDevice] = {}
        self.sio = socketio.Client()
        for d in installation_data["devices"]:
            self.devices[d["name"]] = DaikinDevice(d, self.sio)
        logger.debug("Set up installation '%s'", self.installation_id)

    def connect_installation_socket(self):
        """starts the Socket.IO connection for the provided installation"""

        @self.sio.on("*")
        def catch_all(event, data):
            """Default event handler"""
            logger.debug(
                "Received SocketIO message '%s': %s",
                json.dumps(event),
                json.dumps(data),
            )

        @self.sio.event
        def connect():
            """SIO Connect callback"""
            print("I'm connected!")

        @self.sio.event
        def connect_error(data):
            """SIO Connect Error callback"""
            print("The connection failed!")

        @self.sio.event
        def disconnect():
            """SIO Disonnect callback"""
            print("I'm disconnected!")

        url = f"{self.api.PROD_URL}{self.installation_id}::{self.api.SCOPE}"
        logger.debug("Starting Socket.IO connection: %s", url)
        self.sio.connect(
            url,
            transports=["polling"],
            socketio_path=self.api.SOCKET_PATH,
            headers={"Authorization": f"Bearer {self.api.api_tokens['access_token']}"},
        )
