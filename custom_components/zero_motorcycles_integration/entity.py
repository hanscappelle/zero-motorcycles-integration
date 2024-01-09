"""ZeroEntity class."""
from __future__ import annotations

import json
import os

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import LOGGER
from .coordinator import ZeroCoordinator


class ZeroEntity(CoordinatorEntity):
    """Zero Entity class."""

    _attr_attribution = None

    def __init__(self, coordinator: ZeroCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)

        # get data from manifest here instead, is this the way to go?
        # mostly done so we wouldn't have to change version in several places
        info = json.load(
            open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)), "manifest.json"))
        )
        LOGGER.debug("loaded info %s", info)
        self._attr_attribution = info["attribution"]

        if not coordinator.units:
            LOGGER.debug("no units were fetched, no devices to create here")
        else:
            # 1 entity created with sensors repeated for all units
            self._attr_unique_id = coordinator.config_entry.entry_id
            self._attr_device_info = DeviceInfo(
                identifiers={(info["domain"], self.unique_id)},
                # name="Zero Unit [" + coordinator.units[0]["unitnumber"] + "]",
                name="Zero Motorcycles",  # generic name, not one per unit
                model=info["version"],
                manufacturer=info["name"],
            )
