import datetime
import logging
from enum import Enum
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class MyPyllantEnum(Enum):
    def __str__(self):
        """
        Return 'HOUR' instead of 'DeviceDataBucketResolution.HOUR'
        """
        return self.value

    @property
    def display_value(self) -> str:
        return self.value.replace("_", " ").title()


class CircuitState(MyPyllantEnum):
    HEATING = "HEATING"
    STANDBY = "STANDBY"


class DeviceDataBucketResolution(MyPyllantEnum):
    HOUR = "HOUR"
    DAY = "DAY"
    MONTH = "MONTH"


class ZoneHeatingOperatingMode(MyPyllantEnum):
    MANUAL = "MANUAL"
    TIME_CONTROLLED = "TIME_CONTROLLED"
    OFF = "OFF"


class ZoneCurrentSpecialFunction(MyPyllantEnum):
    NONE = "NONE"
    QUICK_VETO = "QUICK_VETO"
    HOLIDAY = "HOLIDAY"


class ZoneHeatingState(MyPyllantEnum):
    IDLE = "IDLE"
    HEATING_UP = "HEATING_UP"


class DHWCurrentSpecialFunction(MyPyllantEnum):
    CYLINDER_BOOST = "CYLINDER_BOOST"
    REGULAR = "REGULAR"


class DHWOperationMode(MyPyllantEnum):
    MANUAL = "MANUAL"
    TIME_CONTROLLED = "TIME_CONTROLLED"
    OFF = "OFF"


class Zone(BaseModel):
    system_id: str
    name: str
    index: int
    active: bool
    current_room_temperature: float | None
    current_special_function: ZoneCurrentSpecialFunction
    desired_room_temperature_setpoint: float
    manual_mode_setpoint: float
    heating_operation_mode: ZoneHeatingOperatingMode
    heating_state: ZoneHeatingState
    humidity: float | None
    set_back_temperature: float
    time_windows: dict


class Circuit(BaseModel):
    system_id: str
    index: int
    circuit_state: CircuitState
    current_circuit_flow_temperature: float | None
    heating_curve: float | None
    is_cooling_allowed: bool
    min_flow_temperature_setpoint: float | None
    mixer_circuit_type_external: str
    set_back_mode_enabled: bool
    zones: list = []


class DomesticHotWater(BaseModel):
    system_id: str
    index: int
    current_dhw_tank_temperature: float | None
    current_special_function: DHWCurrentSpecialFunction
    max_set_point: float
    min_set_point: float
    operation_mode: DHWOperationMode
    set_point: float
    time_windows: dict


class System(BaseModel):
    id: str
    status: dict[str, bool]
    devices: list["SystemDevice"]
    current_system: dict = {}
    system_configuration: dict = {}
    system_control_state: dict = {}
    gateway: dict = {}
    has_ownership: bool
    zones: list[Zone] = []
    circuits: list[Circuit] = []
    domestic_hot_water: list[DomesticHotWater] = []

    def __init__(self, **data: Any) -> None:
        if len(data["devices"]) > 0 and isinstance(data["devices"][0], dict):
            data["devices"] = [SystemDevice(**d) for d in data.pop("devices")]
        super().__init__(**data)
        logger.debug(
            f'Creating related models from control_state: {self.system_control_state["control_state"]}'
        )
        self.zones = [Zone(system_id=self.id, **z) for z in self._raw_zones]
        self.circuits = [Circuit(system_id=self.id, **c) for c in self._raw_circuits]
        self.domestic_hot_water = [
            DomesticHotWater(system_id=self.id, **d)
            for d in self._raw_domestic_hot_water
        ]

    @property
    def _raw_zones(self) -> list:
        try:
            return self.system_control_state["control_state"].get("zones", [])
        except KeyError:
            logger.info("Could not get zones from system control state")
            return []

    @property
    def _raw_circuits(self) -> list:
        try:
            return self.system_control_state["control_state"].get("circuits", [])
        except KeyError:
            logger.info("Could not get circuits from system control state")
            return []

    @property
    def _raw_domestic_hot_water(self) -> list:
        try:
            return self.system_control_state["control_state"].get(
                "domestic_hot_water", []
            )
        except KeyError:
            logger.info("Could not get domestic hot water from system control state")
            return []

    @property
    def outdoor_temperature(self) -> float | None:
        try:
            return self.system_control_state["control_state"]["general"][
                "outdoor_temperature"
            ]
        except KeyError:
            logger.info(
                "Could not get outdoor temperature from system control state",
            )
            return None

    @property
    def status_online(self) -> bool | None:
        return self.status["online"] if "online" in self.status else None

    @property
    def status_error(self) -> bool | None:
        return self.status["error"] if "error" in self.status else None

    @property
    def water_pressure(self) -> float | None:
        try:
            return self.system_control_state["control_state"]["general"][
                "system_water_pressure"
            ]
        except KeyError:
            logger.info("Could not get water pressure from system control state")
            return None

    @property
    def mode(self) -> str | None:
        try:
            return self.system_control_state["control_state"]["general"]["system_mode"]
        except KeyError:
            logger.info("Could not get mode from system control state")
            return None


class SystemDevice(BaseModel):
    """
    The System contains some information about devices already, this is saved in SystemDevice
    The currentSystem API call returns more device info, which is saved in Device
    """

    system_id: str
    device_id: str | None
    name: str = ""
    type: str = ""
    diagnostic_trouble_codes: list = []
    properties: list = []
    serial_number: str | None
    article_number: str | None
    operational_data: dict = {}
    data: list["DeviceData"] = []

    @property
    def name_display(self) -> str:
        if self.name:
            return self.name
        elif self.device_id:
            return f"Device {self.device_id}"
        elif self.serial_number:
            return f"Device {self.serial_number}"
        else:
            return "System Device"


class Device(SystemDevice):
    system: System
    device_uuid: str
    name: str = ""
    product_name: str
    diagnostic_trouble_codes: list = []
    properties: list = []
    ebus_id: str
    article_number: str
    device_serial_number: str
    device_type: str
    first_data: datetime.datetime
    last_data: datetime.datetime
    operational_data: dict = {}
    data: list["DeviceData"] = []

    def __init__(self, **data):
        data["system_id"] = data["system"].id
        super().__init__(**data)

    @property
    def name_display(self) -> str:
        return self.name if self.name else self.product_name.title()


class DeviceDataBucket(BaseModel):
    start_date: datetime.datetime
    end_date: datetime.datetime
    value: float


class DeviceData(BaseModel):
    def __init__(self, device: Device | None = None, **kwargs: Any) -> None:
        kwargs["data_from"] = kwargs.pop("from") if "from" in kwargs else None
        kwargs["data_to"] = kwargs.pop("to") if "to" in kwargs else None
        super().__init__(device=device, **kwargs)

    device: Device | None
    data_from: datetime.datetime | None
    data_to: datetime.datetime | None
    start_date: datetime.datetime | None
    end_date: datetime.datetime | None
    resolution: DeviceDataBucketResolution | None
    operation_mode: str
    energy_type: str | None
    value_type: str | None
    data: list[DeviceDataBucket] = []


# Updating string type hints for pydantic
System.update_forward_refs()
Device.update_forward_refs()
