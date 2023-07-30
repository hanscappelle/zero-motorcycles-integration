"""ZeroEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION, LOGGER
from .coordinator import ZeroCoordinator


class ZeroEntity(CoordinatorEntity):
    """Zero Entity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: ZeroCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)

        if not coordinator.units:
            LOGGER.debug("no units were fetched, no devices to create here")
        else:
            # 1 entity created with sensors repeated for all units
            self._attr_unique_id = coordinator.config_entry.entry_id
            self._attr_device_info = DeviceInfo(
                identifiers={(DOMAIN, self.unique_id)},
                # name="Zero Unit [" + coordinator.units[0]["unitnumber"] + "]",
                name="Zero Motorcycles",  # generic name, not one per unit
                model=VERSION,
                manufacturer=NAME,
            )
