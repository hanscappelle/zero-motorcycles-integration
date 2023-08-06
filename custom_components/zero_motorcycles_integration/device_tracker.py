"""Support for tracking devices."""
from typing import Optional

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity

from .const import DOMAIN, LOGGER
from .coordinator import ZeroCoordinator
from .entity import ZeroEntity


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up device tracket by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []
    for unit in coordinator.units:
        entities.append(
            ZeroTrackerEntity(
                coordinator=coordinator,
                unitnumber=unit["unitnumber"],
            )
        )
    async_add_entities(entities, True)


class ZeroTrackerEntity(ZeroEntity, TrackerEntity):
    """A class representing a trackable device."""

    def __init__(
        self,
        coordinator: ZeroCoordinator,
        unitnumber: str,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)

        self.unit_number = unitnumber
        LOGGER.debug("init tracker for %s", self.unit_number)

    @property
    def latitude(self) -> Optional[float]:
        """Return latitude value of the device."""
        return self.coordinator.data[self.unit_number][0]["latitude"]

    @property
    def longitude(self) -> Optional[float]:
        """Return longitude value of the device."""
        return self.coordinator.data[self.unit_number][0]["longitude"]

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:crosshairs-gps"

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        heading = self.coordinator.data[self.unit_number][0]["heading"]
        velocity = self.coordinator.data[self.unit_number][0]["velocity"]
        altitude = self.coordinator.data[self.unit_number][0]["altitude"]
        name = self.coordinator.data[self.unit_number][0]["name"]
        return {
            "heading": heading,
            "vin": name,
            "velocity": velocity,
            "altitude": altitude,
        }
