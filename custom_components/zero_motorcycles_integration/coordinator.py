"""DataUpdateCoordinator for zero_motorcycles_integration."""
from __future__ import annotations

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
            update_interval=timedelta(minutes=1),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            # attempt to retrieve unit number
            # return await self.client.async_get_last_transmit()

            # start by getting all units with given login
            units = await self.client.async_get_units()

            # also get last transmit at this point
            LOGGER.debug("received units from API %s", units)

            # for all units get last transmit data
            for unit in units:
                data = await self.client.async_get_last_transmit(unit["unitnumber"])
                LOGGER.debug(
                    "received data for unit %s from API %s", unit["unitnumber"], data
                )
                # TODO figure out how to create devices named per unit (if not already existing)
                # TODO how to set data to sensors

            # create quick access dict here
            return {unit["unitnumber"]: unit for unit in units}

        except ZeroApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except ZeroApiClientError as exception:
            raise UpdateFailed(exception) from exception
