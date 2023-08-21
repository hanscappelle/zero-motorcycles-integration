"""Custom integration to integrate zero_motorcycles_integration with Home Assistant.

For more details about this integration, please refer to
https://github.com/hanscappelle/zero-motorcycles-integration
"""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ZeroApiClient
from .const import DOMAIN, LOGGER
from .coordinator import ZeroCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Provide configuration entry for HomeAssistant framework.

    For us, the configuration entry is the username-password credentials that
    the user needs to access Starcom API.
    """

    # Retrieve the stored credentials from config-flow
    username = entry.data.get(CONF_USERNAME)
    LOGGER.debug("Loaded %s: %s", CONF_USERNAME, username)
    password = entry.data.get(CONF_PASSWORD)
    LOGGER.debug("Loadded %s: ********", CONF_PASSWORD)

    # Initialize the HASS structure
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator = ZeroCoordinator(
        hass=hass,
        client=ZeroApiClient(
            username=username,
            password=password,
            session=async_get_clientsession(hass),
        ),
    )

    # Initiate the coordinator. This method will also make sure to login to the API

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    # configure all sensors
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # alternative with more readable for loop
    # for platform in PLATFORMS:
    #    hass.async_add_job(
    #        hass.config_entries.async_forward_entry_setup(entry, platform)
    #    )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
