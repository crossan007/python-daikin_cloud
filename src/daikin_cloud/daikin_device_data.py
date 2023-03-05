"""Module"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass
class DeviceManufacturer:
    _id: Optional[int] = None
    text: Optional[str] = None


@dataclass_json
@dataclass
class DeviceData:
    machineready: Optional[bool] = None
    version: Optional[str] = None
    aidooit: Optional[bool] = None
    emerheatpresent: Optional[bool] = None
    emerheatstatus: Optional[bool] = None
    fallback: Optional[bool] = None
    t1t2on: Optional[bool] = None
    real_mode: Optional[int] = None
    work_temp_selec_sensor: Optional[int] = None
    stat_channel: Optional[int] = None
    stat_rssi: Optional[int] = None
    stat_ssid: Optional[str] = None
    manufacturer: Optional[DeviceManufacturer] = None
    power: Optional[bool] = None
    mode: Optional[int] = None
    mode_available: Optional[any] = None
    speed_available: Optional[any] = None
    speed_state: Optional[int] = None
    slats_autoud: Optional[bool] = None
    slats_swingud: Optional[bool] = None
    slats_vnum: Optional[int] = None
    range_sp_cool_air_max: Optional[int] = None
    range_sp_cool_air_min: Optional[int] = None
    range_sp_hot_air_max: Optional[int] = None
    range_sp_hot_air_min: Optional[int] = None
    range_sp_auto_air_max: Optional[int] = None
    range_sp_auto_air_min: Optional[int] = None
    device_master_slave: Optional[bool] = None
    master: Optional[bool] = None
    setpoint_step: Optional[bool] = None
    units: Optional[int] = None
    setpoint_air_cool: Optional[int] = None
    setpoint_air_heat: Optional[int] = None
    setpoint_air_auto: Optional[int] = None
    error_value: Optional[int] = None
    error_ascii1: Optional[str] = None
    error_ascii2: Optional[str] = None
    tsensor_error: Optional[bool] = None
    work_temp: Optional[int] = None
    icon: Optional[int] = None
    name: Optional[str] = None
    timezoneId: Optional[str] = None
    isConnected: Optional[bool] = None


@dataclass_json
@dataclass
class DeviceDataMessage:
    mac: Optional[str] = None
    data: Optional[DeviceData] = None
