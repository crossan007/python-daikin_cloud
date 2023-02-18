"""Module"""
import json
import logging
import os
from daikin_api import DaikinAPI
from daikin_installation import DaikinInstallation


class DaikinCloud:
    """Methods to interact with the Daikin One API."""

    data_file = "tmp/daikin.json"
    api: DaikinAPI
    installations: dict[str, DaikinInstallation]

    def __init__(self) -> None:
        self.api = DaikinAPI()
        self.load_environment()
        response = self.api.login_pasword(
            os.environ.get("daikin_email"), os.environ.get("daikin_password")
        )
        self.save_environment()
        logging.debug("Got data %s", json.dumps(response))

    def load_environment(self):
        """Loads tokens from OS environment variables; useful for REPL."""
        try:
            with open(self.data_file, encoding="UTF-8") as read_file:
                data = json.load(read_file)
                self.api.set_tokens(data["tokens"])
        except (KeyError, FileNotFoundError, json.decoder.JSONDecodeError):
            self.token = ""
            self.refresh_token = ""
            logging.debug("No tokens to load from environment")

    def save_environment(self):
        """Saves tokens from OS environment variables; useful for REPL."""
        with open(self.data_file, "w", encoding="UTF-8") as write_file:
            json.dump({"tokens": self.api.get_tokens()}, write_file)
        logging.debug("Saved tokens to environment")

    def fetch_installations(self):
        """Gets installations available to the current user."""
        logging.debug("Getting installations")
        response = self.api.get(f"installations/{self.api.SCOPE}")
        self.installations: dict[str, DaikinInstallation] = {}
        for i in response:
            self.installations[i["_id"]] = DaikinInstallation(self.api, i)
