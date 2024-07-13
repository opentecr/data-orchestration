# Copyright (c) 2024 openTECR Community
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


"""Provide dagster assets."""

from typing import Annotated
from urllib.parse import urlencode

import pandas as pd
from dagster import ConfigurableResource, asset
from pydantic import Field


class GoogleSheetsResource(ConfigurableResource):
    """Define a Google Sheets resource."""

    url: Annotated[
        str,
        Field(
            default="https://docs.google.com/spreadsheets/d/",
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


class SingleSheetResource(ConfigurableResource):
    """Define a single Google sheet resource."""

    sheets: GoogleSheetsResource
    gid: Annotated[str, Field(default=..., description="The individual sheet GID.")]

    def fetch(self) -> pd.DataFrame:
        """Fetch a single Google sheet."""
        params = urlencode({"gid": self.gid, "format": "xlsx"})
        return pd.read_excel(
            f"{self.sheets.url}{self.sheets.spreadsheet_id}/export?{params}",
            engine="openpyxl",
        )


@asset
def opentecr_metadata(metadata_resource: SingleSheetResource):
    """Define the openTECR metadata asset."""
    return metadata_resource.fetch()


@asset
def opentecr_references(references_resource: SingleSheetResource):
    """Define the openTECR references asset."""
    return references_resource.fetch()


@asset
def opentecr_data(data_resource: SingleSheetResource):
    """Define the openTECR data asset."""
    return data_resource.fetch()


@asset
def opentecr_comments(comments_resource: SingleSheetResource):
    """Define the openTECR comments asset."""
    return comments_resource.fetch()
