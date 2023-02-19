"""Daikin API class"""
from logger import logger
import requests
from typing_extensions import TypedDict

APITokens = TypedDict("APITokens", {"access_token": str, "refresh_token": str})

# TODO:self.authHeader = headers["Authorization"] in charles_dev/tmp/site-packages/engineio/client.py


class DaikinAPI:
    """Commands for interacting with REST and Socket.IO"""

    api_tokens: APITokens
    timeout_seconds = 5
    PROD_URL = "https://dkncloudna.com/"
    API_VERSION = "api/v1/"
    SCOPE = "dknUsa"
    SOCKET_PATH = "/api/v1/devices/socket.io/"

    def __init__(self) -> None:
        self.api_tokens = {}

    def build_headers(self, headers: dict = None, auth: bool = True):
        """Creates headers for API requests"""
        if headers is None:
            headers = {}
        headers["Access-Control-Allow-Origin"] = "*"
        if auth:
            headers["Authorization"] = f"Bearer {self.api_tokens['access_token']}"
        return headers

    def post(
        self, subpath: str, headers: dict = None, body: dict = None, auth: bool = True
    ):
        """Proxy api post method."""
        headers = self.build_headers(headers, auth)
        url = f"{self.PROD_URL}{self.API_VERSION}{subpath}"
        logger.debug("API POST to %s", url)
        request = requests.post(
            url,
            headers=headers,
            json=body,
            timeout=self.timeout_seconds,
        )
        return request.json()

    def get(self, subpath: str, headers: dict = None, auth: bool = True):
        """Proxy api get method."""
        headers = self.build_headers(headers, auth)
        url = f"{self.PROD_URL}{self.API_VERSION}{subpath}"
        logger.debug("API GET to %s", url)
        request = requests.get(
            url,
            headers=headers,
            timeout=self.timeout_seconds,
        )
        return request.json()

    def login_pasword(self, email: str, password: str):
        """Logs in and gets a token / refreshtoken."""
        if "access_token" in self.api_tokens and self.api_tokens["access_token"]:
            logger.debug("Already logged in")
            return

        if email is None:
            raise ValueError("No email address")
        if password is None:
            raise ValueError("No password")

        login_path = f"auth/login/{self.SCOPE}"
        logger.debug("logger in")
        response = self.post(
            login_path, body={"email": email, "password": password}, auth=False
        )
        self.api_tokens = {
            "access_token": response["token"],
            "refresh_token": response["refreshToken"],
        }
        logger.debug("Login Success")
        return {
            "profile": response["data"],
            "installations": response["scope"][self.SCOPE]["installations"],
        }

    def set_tokens(self, api_tokens: APITokens):
        """Sets api tokens"""
        self.api_tokens = api_tokens

    def get_tokens(self) -> APITokens:
        """gets api tokens"""
        return self.api_tokens

    def update_token(self):
        """Updates the current token using the refresh token."""
        response = self.get(
            f"auth/refreshToken/{self.api_tokens['refresh_token']}/{self.SCOPE}"
        )
        logger.debug(
            "Updating access token using refresh token %s",
            self.api_tokens["refresh_token"],
        )
        self.api_tokens["access_token"] = response["token"]
        self.api_tokens["refresh_token"] = response["refreshToken"]
        logger.debug("Token refresh success")
