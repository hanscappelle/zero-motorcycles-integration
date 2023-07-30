"""Sensor platform for zero_motorcycles_integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import DOMAIN, LOGGER
from .coordinator import ZeroCoordinator
from .entity import ZeroEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="zero_motorcycles",
        name="soc",
        icon="mdi:battery-charging-50",
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
        name="gps_valid",
        icon="mdi:crosshairs-gps",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="gps_connected",
        icon="mdi:crosshairs-gps",
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
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="tipover",
        icon="mdi:chat-alert",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="charging",
        icon="mdi:ev-station",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="chargecomplete",
        icon="mdi:battery-charging-100",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="pluggedin",
        icon="mdi:power-plug",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="chargingtimeleft",
        icon="mdi:battery-clock",
    ),
    SensorEntityDescription(
        key="zero_motorcycles",
        name="storage",
        icon="mdi:sleep",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        ZeroSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class ZeroSensor(ZeroEntity, SensorEntity):
    """zero_motorcycles_integration Sensor class."""

    def __init__(
        self,
        coordinator: ZeroCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        # had to create unique IDs per sensor here, using key.name
        unitnumber = self.coordinator.units[0]["unitnumber"]
        self._attr_unique_id = (
            entity_description.key + "." + unitnumber + "." + entity_description.name
        )
        self.entity_description = entity_description

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        sensor = self.entity_description.name
        unitnumber = self.coordinator.units[0]["unitnumber"]
        value = self.coordinator.data[unitnumber][0][sensor]
        LOGGER.debug(
            "Sensor value for %s is %s",
            self.unique_id,
            value,
        )
        return value
