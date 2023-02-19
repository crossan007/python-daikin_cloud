"""Module: """
import json
from logger import logger
import socketio
from daikin_device import DaikinDevice

class DaikinInstallation:
    """Class for interacting with an installation"""

    installation_socket: socketio.Client
    api: any
    installation_id: str
    devices: dict[str, DaikinDevice]

    def __init__(self, api, installation_data) -> None:
        """Sets up this installation"""
        self.api = api
        self.devices = []
        self.installation_id = installation_data["_id"]
        self.devices: dict[str, DaikinDevice] = {}
        self.installation_socket = socketio.Client()
        for d in installation_data["devices"]:
            self.devices[d["name"]] = DaikinDevice(d, self.installation_socket)
        logger.debug("Set up installation '%s'", self.installation_id)

    def connect_installation_socket(self):
        """starts the Socket.IO connection for the provided installation"""

        @self.installation_socket.on("*")
        def catch_all(event, data):
            """Default event handler"""
            logger.debug(
                "Installation socket message '%s': %s",
                json.dumps(event),
                json.dumps(data),
            )

        @self.installation_socket.event
        def connect():
            """installation_socket Connect callback"""
            logger.debug("Installation socket connected!")

        @self.installation_socket.event
        def connect_error(data):
            """installation_socket Connect Error callback"""
            logger.debug("Installation socket connection failed!")

        @self.installation_socket.event
        def disconnect():
            """installation_socket Disonnect callback"""
            logger.debug("Installation socketdisconnected!")

        url = f"{self.api.PROD_URL}{self.installation_id}::{self.api.SCOPE}"
        logger.debug("Starting : %s", url)
        self.installation_socket.connect(
            url,
            transports=["polling"],
            socketio_path=self.api.SOCKET_PATH,
            headers={"Authorization": f"Bearer {self.api.api_tokens['access_token']}"},
        )
