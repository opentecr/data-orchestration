from typing import Annotated
from urllib.parse import urlencode

import pandas as pd
from dagster import ConfigurableResource
from pydantic import Field


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
            default=...,
            description="The Google Sheets spreadsheet ID.",
        ),
    ]

    def url(self, gid: str) -> str:
        """Return the URL of the Google sheet."""
        params = urlencode({"gid": gid, "format": "xlsx"})
        return f"{self.base_url}/{self.spreadsheet_id}/export?{params}"

    def fetch(self, gid: str) -> pd.DataFrame:
        """Fetch a single Google sheet."""
        return pd.read_excel(self.url(gid=gid), engine="openpyxl")
