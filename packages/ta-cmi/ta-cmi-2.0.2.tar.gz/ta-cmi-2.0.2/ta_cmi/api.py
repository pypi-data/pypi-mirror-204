import json
from typing import Any, Dict

import yarl
from aiohttp import BasicAuth, ClientConnectionError, ClientSession

from .const import HTTP_UNAUTHORIZED


class API:
    """Class to perform basic API requests."""

    def __init__(self, session: ClientSession = None, auth: BasicAuth = None) -> None:
        """Initialize."""
        self.session = session
        self._auth = auth

        self._internal_session = False

    async def _make_request(self, url: str) -> Dict[str, Any]:
        """Retrieve json data from REST endpoint."""
        raw_response: str = await self._make_request_no_json(url)

        if not len(raw_response):
            return {}

        return json.loads(raw_response)

    async def _make_request_no_json(self, url: str) -> str:
        """Retrieve data from REST endpoint."""
        if self.session is None:
            self._internal_session = True
            self.session = ClientSession()

        try:
            async with self.session.get(url, auth=self._auth) as res:
                await self._close_session()

                if res.status == HTTP_UNAUTHORIZED:
                    raise InvalidCredentialsError("Invalid credentials")
                elif res.status >= 300:
                    raise ApiError(
                        f"Invalid response from {res.url.host}: {res.status}"
                    )

                text = await res.text()
                return text
        except ClientConnectionError:
            await self._close_session()
            raise ApiError(f"Could not connect to {yarl.URL(url).host}")

    async def _close_session(self) -> None:
        """Close the internal session."""
        if self._internal_session:
            await self.session.close()
            self.session = None


class ApiError(Exception):
    """Raised when API request ended in error."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status


class InvalidCredentialsError(Exception):
    """Triggered when the credentials are invalid."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status
