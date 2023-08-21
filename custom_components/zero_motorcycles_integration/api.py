"""Mongol or starcom API used by Zero Motorcycles for sharing data.

For more details about this starcom API please refer to
https://bitbucket.org/cappelleh/zengo-android/src/master/
"""

from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout


class ZeroApiClientError(Exception):
    """Exception to indicate a general API error."""


class ZeroApiClientCommunicationError(ZeroApiClientError):
    """Exception to indicate a communication error."""


class ZeroApiClientAuthenticationError(ZeroApiClientError):
    """Exception to indicate an authentication error."""


class ZeroApiClient:
    """Starcom API used by Zero Motorcycles for sharing data."""

    def __init__(
        self,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Set user credentials for API."""
        self._username = username
        self._password = password
        self._session = session

    async def async_get_units(self) -> any:
        """Get available unit numbers for given credentials from API."""
        return await self._api_wrapper(
            method="get",
            url="https://mongol.brono.com/mongol/api.php?commandname=get_units&format=json&user="
            + self._username
            + "&pass="
            + self._password,
        )

    async def async_get_last_transmit(self, unitnumber) -> any:
        """Get available available data from API."""
        return await self._api_wrapper(
            method="get",
            url="https://mongol.brono.com/mongol/api.php?commandname=get_last_transmit&format=json&user="
            + self._username
            + "&pass="
            + self._password
            + "&unitnumber="
            + unitnumber,
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (401, 403, 601):
                    raise ZeroApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.json()

        except asyncio.TimeoutError as exception:
            raise ZeroApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise ZeroApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise ZeroApiClientError("Something really wrong happened!") from exception
