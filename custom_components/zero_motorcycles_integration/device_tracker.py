"""Support for tracking devices."""

from homeassistant.components.device_tracker.const import SourceType
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
    def latitude(self) -> float | type(None):
        """Return latitude value of the device."""
        return self.coordinator.data[self.unit_number][0]["latitude"]

    @property
    def longitude(self) -> float | type(None):
        """Return longitude value of the device."""
        return self.coordinator.data[self.unit_number][0]["longitude"]

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SourceType.GPS

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
        gps_connected = self.coordinator.data[self.unit_number][0]["gps_connected"]
        gps_valid = self.coordinator.data[self.unit_number][0]["gps_valid"]
        satellites = self.coordinator.data[self.unit_number][0]["satellites"]
        name = self.coordinator.data[self.unit_number][0]["name"]
        return {
            "heading": heading,
            "vin": name,
            "velocity": velocity,
            "altitude": altitude,
            "gps_connected": gps_connected,
            "gps_valid": gps_valid,
            "satellites": satellites,
        }
