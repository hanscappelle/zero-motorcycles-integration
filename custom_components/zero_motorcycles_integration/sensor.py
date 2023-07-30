"""Sensor platform for zero_motorcycles_integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import DOMAIN, LOGGER
from .coordinator import ZeroCoordinator
from .entity import ZeroEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="zero_motorcycles_integration",
        name="SOC",
        icon="mdi:battery-charging-50",
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
    # TODO create more sensors here


class ZeroSensor(ZeroEntity, SensorEntity):
    """zero_motorcycles_integration Sensor class."""

    def __init__(
        self,
        coordinator: ZeroCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        unitnumber = self.coordinator.units[0]["unitnumber"]
        soc = self.coordinator.data[unitnumber][0]["soc"]
        LOGGER.debug(
            "SOC sensor value for unit %s is %s from %s ",
            unitnumber,
            soc,
            self.coordinator.data,
        )
        return soc
