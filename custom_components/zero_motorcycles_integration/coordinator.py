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
    """Class to manage fetching data from API."""

    config_entry: ConfigEntry
    units = {}  # all units fetched

    def __init__(
        self,
        hass: HomeAssistant,
        client: ZeroApiClient,
    ) -> None:
        """Initialize."""
        self.client = client

        # TODO maybe keep track of vehicles instead of mapping data
        # self.vehicles = None
        self.data = {}

        # TODO get scan interval from config
        # check options https://developers.home-assistant.io/docs/config_entries_options_flow_handler
        # scan_interval = timedelta(
        #    seconds=config_entry.options.get(
        #        CONF_SCAN_INTERVAL,
        #        config_entry.data.get(
        #            CONF_SCAN_INTERVAL, SCAN_INTERVAL.total_seconds()
        #        ),
        #    )
        # )
        # apply configured refresh interval here
        # super().__init__(hass, LOGGER, name=DOMAIN, update_interval=scan_interval)

        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """Update data using API."""
        try:
            # start by getting all units with given login
            self.units = await self.client.async_get_units()

            # also get last transmit at this point
            LOGGER.debug("received units from API %s", self.units)

            # for all units get last transmit data
            data = {}
            for unit in self.units:
                unitnumber = unit["unitnumber"]
                # create quick access dict here
                data[unitnumber] = await self.client.async_get_last_transmit(unitnumber)
                # LOGGER.debug(
                #    "received data for unit %s from API %s",
                #    unitnumber,
                #    data[unitnumber],
                # )

            return data

        except ZeroApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except ZeroApiClientError as exception:
            raise UpdateFailed(exception) from exception
