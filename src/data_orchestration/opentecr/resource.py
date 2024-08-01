from typing import Annotated
from urllib.parse import urlencode

import httpx
from dagster import ConfigurableResource
from pydantic import Field
from upath import UPath


class GoogleSheetsResource(ConfigurableResource):
    """Define a Google Sheets resource."""

    base_url: Annotated[
        str,
        Field(
            default="https://docs.google.com/spreadsheets/d",
            description="The Google Sheets base URL.",
        ),
    ]
    spreadsheet_id: Annotated[
        str,
        Field(
            default="1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c",
            description="The Google Sheets spreadsheet ID.",
        ),
    ]
    base_path: Annotated[
        str,
        Field(
            default=".",
            description="The base path where to store Excel files.",
        ),
    ]

    def url(self, gid: str) -> str:
        """Return the URL of the Google sheet."""
        params = urlencode({"gid": gid, "format": "xlsx"})
        return f"{self.base_url}/{self.spreadsheet_id}/export?{params}"

    def _fetch_excel(self, client: httpx.Client, gid: str) -> UPath:
        """Fetch a single Google sheet as Excel and return its file path."""
        result = UPath(self.base_path) / f"{gid}.xlsx"

        with (
            client.stream(
                method="GET",
                url=self.url(gid=gid),
                follow_redirects=True,
            ) as response,
            result.open(mode="wb") as handle,
        ):
            response.raise_for_status()
            for data in response.iter_bytes():
                handle.write(data)
        return result

    def fetch(self, gid: str) -> UPath:
        """Fetch a single Google sheet as Excel and return its file path."""
        with httpx.Client(timeout=httpx.Timeout(10.0, read=30.0, pool=None)) as client:
            return self._fetch_excel(client=client, gid=gid)
