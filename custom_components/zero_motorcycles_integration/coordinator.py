"""DataUpdateCoordinator for zero_motorcycles_integration."""
from __future__ import annotations

import logging

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .api import (
    ZeroApiClient,
    ZeroApiClientAuthenticationError,
    ZeroApiClientError,
)
from .const import DOMAIN, LOGGER

_LOGGER = logging.getLogger(__name__)


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class ZeroCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: ZeroApiClient,
    ) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            # attempt to retrieve unit number
            # return await self.client.async_get_last_transmit()

            # start by getting all units with given login
            units = await self.client.async_get_units()

            # TODO also get last transmit at this point
            _LOGGER.info("received units from API %s", units)

            # create quick access dict here
            return {unit["unitnumber"]: unit for unit in units}

        except ZeroApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except ZeroApiClientError as exception:
            raise UpdateFailed(exception) from exception
