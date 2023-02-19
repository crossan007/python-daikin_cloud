"""Module"""
import json
from logger import logger
import os
import socketio
from daikin_api import DaikinAPI
from daikin_installation import DaikinInstallation


class DaikinCloud:
    """Methods to interact with the Daikin One API."""

    data_file = "tmp/daikin.json"
    api: DaikinAPI
    installations: dict[str, DaikinInstallation]
    user_socket: socketio.Client

    def __init__(self) -> None:
        self.api = DaikinAPI()
        self.user_socket = socketio.Client()
        self.load_environment()
        response = self.api.login_pasword(
            os.environ.get("daikin_email"), os.environ.get("daikin_password")
        )
        self.save_environment()
        logger.debug("Got data %s", json.dumps(response))
        self.fetch_installations()
        self.connect_user_socket()

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

    def fetch_installations(self):
        """Gets installations available to the current user."""
        logger.debug("Getting installations")
        response = self.api.get(f"installations/{self.api.SCOPE}")
        self.installations: dict[str, DaikinInstallation] = {}
        for i in response:
            self.installations[i["_id"]] = DaikinInstallation(self.api, i)

    def connect_user_socket(self):
        """connects the user socket"""

        @self.user_socket.on("*", namespace="/users")
        def catch_all(event, data):
            """Default event handler"""
            logger.debug(
                "User socket message '%s': %s",
                json.dumps(event),
                json.dumps(data),
            )

        @self.user_socket.event
        def connect(namespace="/users"):
            """SIO Connect callback"""
            logger.debug("User socket connected!")

        @self.user_socket.event
        def connect_error(data, namespace="/users"):
            """SIO Connect Error callback"""
            logger.debug("User socket connection failed!")

        @self.user_socket.event
        def disconnect(namespace="/users"):
            """SIO Disonnect callback"""
            logger.debug("User socket disconnected!")

        url = f"{self.api.API_URL}"
        logger.debug("Starting user socket: %s", url)
        self.user_socket.connect(
            url,
            namespaces=["/users"],
            transports=["polling"],
            socketio_path=self.api.SOCKET_PATH,
            headers={"Authorization": f"Bearer {self.api.api_tokens['access_token']}"},
        )
