"""Module: """
import json
from logger import logger
import socketio
from daikin_device import DaikinDevice
from daikin_api import DaikinAPI
from daikin_device_data import DeviceDataMessage


class DaikinInstallation:
    """Class for interacting with an installation"""

    installation_socket: socketio.AsyncClient
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
        self.installation_socket = socketio.AsyncClient()
        for d in installation_data["devices"]:
            self.devices[d["mac"]] = DaikinDevice(d, self)
            logger.debug(
                "Set up device '%s':'%s' in installation '%s'",
                d["name"],
                d["mac"],
                self.installation_id,
            )
        logger.debug("Set up installation '%s'", self.installation_id)

    async def emit(self, event, data, callback):
        """Proxies the Socket.IO emit but includes this installation's namespace"""
        await self.installation_socket.emit(
            event, data, namespace=self.installation_namespace, callback=callback
        )

    async def connect_installation_socket(self):
        """starts the Socket.IO connection for the provided installation"""

        url = f"{self.api.API_URL}"
        # url = "http://172.30.9.155:3000"

        logger.debug(
            "Starting installation socket: %s; namespace: '%s'",
            url,
            self.installation_namespace,
        )
        await self.installation_socket.connect(
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
            device_data_message: DeviceDataMessage = DeviceDataMessage.from_dict(data)
            try:
                self.devices[device_data_message.mac].handle_device_data(
                    device_data_message.data
                )
            except KeyError:
                logger.warning(
                    "Device '%s' does not exist in installation '%s'",
                    device_data_message.mac,
                    self.installation_id,
                )

        @self.installation_socket.event(namespace=self.installation_namespace)
        def message(data):
            logger.debug("Installation socket message '%s'", data)

        @self.installation_socket.event
        def connect():
            """installation_socket Connect callback"""
            logger.debug(
                "Installation socket connected: '%s'",
                self.installation_namespace,
            )

        @self.installation_socket.event
        def connect_error(data):
            """installation_socket Connect Error callback"""
            logger.debug("Installation socket connection failed!")

        @self.installation_socket.event
        def disconnect():
            """installation_socket Disonnect callback"""
            logger.debug("Installation socketdisconnected!")
