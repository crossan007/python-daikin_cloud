"""Module: """
from __future__ import annotations
from logger import logger
from typing import TYPE_CHECKING
from dataclasses import fields

from collections.abc import Callable
import json
from daikin_device_data import DeviceData

if TYPE_CHECKING:
    from daikin_installation import DaikinInstallation


class DaikinDevice:
    """Class for interacting with device"""

    mac: str
    icon: str
    name: str
    acs_mode: bool
    installation: DaikinInstallation
    device_data: DeviceData
    on_data_updated: list[Callable[[]]]

    def __init__(self, device_data: any, installation: DaikinInstallation) -> None:
        self.acs_mode = False
        self.name = device_data["name"]
        self.icon = device_data["icon"]
        self.mac = device_data["mac"]
        self.installation = installation
        self.device_data = DeviceData()
        self.on_data_updated = []
        logger.debug("Setup device %s - %s", self.name, self.mac)

    async def set_device_value(self, prop: str, value: str):
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

        await self.installation.emit(
            "create-machine-event", update_command, callback=callback_fun
        )
        setattr(self.device_data, prop, value)

    def add_update_callback(self, callback: Callable[[]]):
        """Updates the callback and then calls it"""
        self.on_data_updated.append(callback)
        self._invoke_callback()

    def handle_device_data(self, data: DeviceData):
        """Update this device model with new data from Daikin Cloud"""
        logger.debug("Got device Data for '%s'", self.name)
        changes = False
        for field in fields(data):
            new_value = getattr(data, field.name)
            if new_value is not None:
                setattr(self.device_data, field.name, new_value)
                logger.debug(
                    "Device property '%s' changed to '%s'", field.name, new_value
                )
                changes = True
        if changes:
            if hasattr(self, "on_data_updated") and self.on_data_updated is not None:
                self._invoke_callback()

    def _invoke_callback(self):
        if self.on_data_updated.__len__ == 0:
            logger.debug("No callbacks registered")
            return

        logger.debug("Notifying al on_data_updated callbacks of changes")
        for callback in self.on_data_updated:
            try:
                callback()
            except Exception:
                logger.exception("Failed to execute a callback")
