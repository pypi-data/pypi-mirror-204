from typing import Any, Dict

from aiohttp import ClientSession

from .api import API
from .const import _LOGGER


class CoEAPI(API):
    """Class to perform API requests to the CoE Addon."""

    COE_DATA = "/"

    def __init__(self, host: str, session: ClientSession = None) -> None:
        """Initialize."""
        super().__init__(session)

        self.host = host

    async def get_coe_data(self) -> Dict[str, Any] | None:
        """Get the CoE data."""
        _LOGGER.debug("Receive data from CoE server")

        url = f"{self.host}{self.COE_DATA}"
        data = await self._make_request(url)

        _LOGGER.debug("Received data from CoE server: %s", data)

        if len(data) == 0:
            return None

        return data
