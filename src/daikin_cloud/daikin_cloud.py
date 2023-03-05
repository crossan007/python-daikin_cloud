"""
Module

TODO: Figure out dependency import paths
using sys.path.append("/workspaces/core/charles_dev") isn't goning to work for prod


"""
import sys

sys.path.append("/workspaces/core/charles_dev")
import json
from logger import logger
import os
import socketio
from daikin_api import DaikinAPI
from daikin_installation import DaikinInstallation
from daikin_device import DaikinDevice
from daikin_profile import DaikinProfile


class DaikinCloud:
    """Methods to interact with the Daikin One API."""

    data_file = "tmp/daikin.json"
    api: DaikinAPI
    installations: dict[str, DaikinInstallation]
    devices: list[DaikinDevice]
    user_socket: socketio.AsyncClient
    profile: DaikinProfile

    def __init__(self) -> None:
        self.api = DaikinAPI()
        self.user_socket = socketio.AsyncClient()
        self.devices = []

    async def after_login(self):
        await self.fetch_installations()
        await self.connect_user_socket()

    async def login_dev(self):
        self.load_environment()
        email = os.environ.get("daikin_email")
        password = os.environ.get("daikin_password")
        response = await self.api.login_pasword(email, password)
        self.profile = response["profile"]
        self.save_environment()
        await self.after_login()

    async def login(self, email: str, password: str):
        response = await self.api.login_pasword(email, password)
        self.profile = response["profile"]
        await self.after_login()

    def load_environment(self):
        """Loads tokens from OS environment variables; useful for REPL."""
        try:
            with open(self.data_file, encoding="UTF-8") as read_file:
                data = json.load(read_file)
                self.api.set_tokens(data["tokens"])
        except (KeyError, FileNotFoundError, json.decoder.JSONDecodeError):
            self.token = ""
            self.refresh_token = ""
            logger.debug("No tokens to load from environment")

    def save_environment(self):
        """Saves tokens from OS environment variables; useful for REPL."""
        with open(self.data_file, "w", encoding="UTF-8") as write_file:
            json.dump({"tokens": self.api.get_tokens()}, write_file)
        logger.debug("Saved tokens to environment")

    async def fetch_installations(self):
        """Gets installations available to the current user."""
        logger.debug("Getting installations")
        response = await self.api.get(f"installations/{self.api.SCOPE}")
        self.installations: dict[str, DaikinInstallation] = {}
        for i in response:
            thisInstallation = DaikinInstallation(self.api, i)
            await thisInstallation.connect_installation_socket()
            self.installations[i["_id"]] = thisInstallation
            self.devices.extend(thisInstallation.devices.values())

    async def connect_user_socket(self):
        """connects the user socket"""

        @self.user_socket.event(namespace="/users")
        def message(data):
            logger.debug("User socket event: '%s'", json.dumps(data))

        @self.user_socket.on("*")
        def catch_all(event, data):
            """Default event handler"""
            logger.debug(
                "User socket message '%s': %s",
                json.dumps(event),
                json.dumps(data),
            )

        @self.user_socket.event(namespace="/users")
        def connect():
            """SIO Connect callback"""
            logger.debug("User socket connected!")

        @self.user_socket.event(namespace="/users")
        def connect_error(data):
            """SIO Connect Error callback"""
            logger.debug("User socket connection failed!")

        @self.user_socket.event(namespace="/users")
        def disconnect():
            """SIO Disonnect callback"""
            logger.debug("User socket disconnected!")

        url = f"{self.api.API_URL}"
        logger.debug("Starting user socket: %s", url)
        await self.user_socket.connect(
            url,
            namespaces=["/users"],
            transports=["polling"],
            socketio_path=self.api.SOCKET_PATH,
            headers={"Authorization": f"Bearer {self.api.api_tokens['access_token']}"},
        )
