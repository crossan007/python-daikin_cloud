"""Module: """
import json
from logger import logger
import socketio
from daikin_device import DaikinDevice
from daikin_api import DaikinAPI


class DaikinInstallation:
    """Class for interacting with an installation"""

    installation_socket: socketio.Client
    api: DaikinAPI
    installation_id: str
    devices: dict[str, DaikinDevice]
    installation_namespace: str

    def __init__(self, api, installation_data) -> None:
        """Sets up this installation"""
        self.api = api
        self.devices = []
        self.installation_id = installation_data["_id"]
        self.devices: dict[str, DaikinDevice] = {}
        self.installation_namespace = f"/{self.installation_id}::{self.api.SCOPE}"
        self.installation_socket = socketio.Client()
        for d in installation_data["devices"]:
            self.devices[d["name"]] = DaikinDevice(
                d, self.installation_socket, self.installation_namespace
            )
            logger.debug(
                "Set up device '%s':'%s' in installation '%s'",
                d["name"],
                d["mac"],
                self.installation_id,
            )
        logger.debug("Set up installation '%s'", self.installation_id)

        self.connect_installation_socket()

    def connect_installation_socket(self):
        """starts the Socket.IO connection for the provided installation"""

        url = f"{self.api.API_URL}"
        # url = "http://172.30.9.155:3000"

        logger.debug(
            "Starting installation socket: %s; namespace: '%s'",
            url,
            self.installation_namespace,
        )
        self.installation_socket.connect(
            url,
            transports=["polling"],
            namespaces=[self.installation_namespace],
            socketio_path=self.api.SOCKET_PATH,
            headers={"Authorization": f"Bearer {self.api.api_tokens['access_token']}"},
        )

        @self.installation_socket.on("*", namespace=self.installation_namespace)
        def catch_all(event, data):
            """Default event handler"""
            logger.debug(
                "Installation socket message '%s': %s",
                json.dumps(event),
                json.dumps(data),
            )

        @self.installation_socket.on(
            "device-data", namespace=self.installation_namespace
        )
        def on_device_data(data):
            logger.debug("Got device data:  %s", json.dumps(data))

        @self.installation_socket.event(namespace=self.installation_namespace)
        def message(data):
            logger.debug("Installation socket message '%s'", data)

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
