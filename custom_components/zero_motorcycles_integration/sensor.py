"""Sensor platform for zero_motorcycles_integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
)
from homeassistant.const import UnitOfLength, UnitOfSpeed, UnitOfElectricPotential, UnitOfTime, PERCENTAGE

from .const import DOMAIN, LOGGER
from .coordinator import ZeroCoordinator
from .entity import ZeroEntity

SENSORS = (
    SensorEntityDescription(
        key="zero_motorcycles",
        name="soc",
        icon="mdi:battery-charging-50",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="name",
        icon="mdi:id-card",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="mileage",
        icon="mdi:gauge",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="software_version",
        icon="mdi:bug",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="longitude",
        icon="mdi:map-marker",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="latitude",
        icon="mdi:map-marker",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="altitude",
        icon="mdi:image-filter-hdr",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="satellites",
        icon="mdi:satellite-variant",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="velocity",
        icon="mdi:gauge",
        device_class=SensorDeviceClass.SPEED,
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="heading",
        icon="mdi:compass",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="main_voltage",
        icon="mdi:car-battery",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="chargingtimeleft",
        icon="mdi:battery-clock",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # create sensors for all units found, not just the first one
    # work with an array of devices
    devices = []

    for unit in coordinator.units:
        for sensor in SENSORS:
            devices.append(
                ZeroSensor(
                    coordinator=coordinator,
                    entity_description=sensor,
                    unitnumber=unit["unitnumber"],
                    sensor_name=sensor.name,
                )
            )

    async_add_devices(devices, True)


class ZeroSensor(ZeroEntity, SensorEntity):
    """zero_motorcycles_integration Sensor class."""

    def __init__(
        self,
        coordinator: ZeroCoordinator,
        entity_description: SensorEntityDescription,
        unitnumber: str,
        sensor_name: str,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)

        # set unit number for unit reference here, this is used as a key in received data
        self.unitnumber = unitnumber
        self.sensor_name = sensor_name  # used for data point refererence

        # had to create unique IDs per sensor here, using key.name
        self._attr_unique_id = (
            entity_description.key + "." + unitnumber + "." + entity_description.name
        )
        self._name = unitnumber + " " + entity_description.name
        # make names unique per unit
        # entity_description.name = sensor_name + "." + unitnumber
        # entity_description.key = "unit." + unitnumber + "." + entity_description.name
        self.entity_description = entity_description

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        # value = self.coordinator.data[self.unitnumber][0][sensor]
        value = self.coordinator.data[self.unitnumber][0][self.sensor_name]
        LOGGER.debug(
            "Sensor value for %s is %s",
            self.unique_id,
            value,
        )
        return value
