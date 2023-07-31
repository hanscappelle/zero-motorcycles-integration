"""Binary sensor platform for integration_blueprint."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .const import DOMAIN, LOGGER
from .coordinator import ZeroCoordinator
from .entity import ZeroEntity

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="zero_motorcycles",
        name="tipover",
        icon="mdi:chat-alert",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    BinarySensorEntityDescription(
        key="zero_motorcycles",
        name="gps_valid",
        icon="mdi:crosshairs-gps",
        device_class=BinarySensorDeviceClass.PROBLEM,
    ),
    BinarySensorEntityDescription(
        key="zero_motorcycles",
        name="gps_connected",
        icon="mdi:crosshairs-gps",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
    BinarySensorEntityDescription(
        key="zero_motorcycles",
        name="charging",
        icon="mdi:ev-station",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
    ),
    BinarySensorEntityDescription(
        key="zero_motorcycles",
        name="chargecomplete",
        icon="mdi:battery-charging-100",
    ),
    BinarySensorEntityDescription(
        key="zero_motorcycles",
        name="pluggedin",
        icon="mdi:power-plug",
        device_class=BinarySensorDeviceClass.PLUG,
    ),
    BinarySensorEntityDescription(
        key="zero_motorcycles",
        name="storage",
        icon="mdi:sleep",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # create sensors for all units found, not just the first one
    for unit in coordinator.units:
        async_add_devices(
            ZeroBinarySensor(
                coordinator=coordinator,
                entity_description=entity_description,
                unitnumber=unit["unitnumber"],
            )
            for entity_description in ENTITY_DESCRIPTIONS
        )


class ZeroBinarySensor(ZeroEntity, BinarySensorEntity):
    """integration_blueprint binary_sensor class."""

    unitnumber: str  # each motorcycle gets this unique unit number assigned

    def __init__(
        self,
        coordinator: ZeroCoordinator,
        entity_description: BinarySensorEntityDescription,
        unitnumber: str,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.unitnumber = unitnumber
        # had to create unique IDs per sensor here, using key.name
        self._attr_unique_id = (
            entity_description.key + "." + unitnumber + "." + entity_description.name
        )
        # make names unique per unit
        entity_description.name = (
            entity_description.name.split(".")[0] + "." + unitnumber
        )
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        sensor = self.entity_description.name
        value = self.coordinator.data[self.unitnumber][0][sensor.split(".")[0]]
        LOGGER.debug(
            "Sensor value for %s is %s",
            self.unique_id,
            value,
        )
        return value
