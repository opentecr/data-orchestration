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

from typing import Annotated, Any
from urllib.parse import urlencode

import pandas as pd
from dagster import (
    ConfigurableResource,
    MetadataValue,
    Output,
    asset,
)
from pandera.typing import DataFrame
from pydantic import Field

from .types import (
    OpenTECRData,
    OpenTECRDataDT,
    OpenTECRReference,
    OpenTECRReferenceDT,
    OpenTECRTableComment,
    OpenTECRTableCommentDT,
    OpenTECRTableMetadata,
    OpenTECRTableMetadataDT,
)


class GoogleSheetsResource(ConfigurableResource):
    """Define a Google Sheets resource."""

    base_url: Annotated[
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

    @property
    def url(self) -> str:
        """Return the URL of the Google sheet."""
        params = urlencode({"gid": self.gid, "format": "xlsx"})
        return f"{self.sheets.base_url}{self.sheets.spreadsheet_id}/export?{params}"

    def fetch(self) -> pd.DataFrame:
        """Fetch a single Google sheet."""
        return pd.read_excel(self.url, engine="openpyxl")


def table_metadata(df: DataFrame) -> dict[str, Any]:
    """Return the metadata of a table."""
    # The conversion to `object` type and `fillna` are workarounds for
    #  https://github.com/astanin/python-tabulate/issues/316.
    return {
        "dagster/row_count": len(df),
        "dagster/column_count": len(df.columns),
        "head": MetadataValue.md(df.head(n=5).astype(object).fillna("").to_markdown()),
        "tail": MetadataValue.md(df.tail(n=5).astype(object).fillna("").to_markdown()),
    }


@asset
def opentecr_metadata(
    metadata_resource: SingleSheetResource,
) -> Output[OpenTECRTableMetadataDT]:
    """Define the openTECR metadata asset."""
    result = OpenTECRTableMetadata.validate(metadata_resource.fetch())
    return Output(
        result,
        metadata={
            **table_metadata(result),
            "source": MetadataValue.url(metadata_resource.url),
        },
    )


@asset
def opentecr_references(
    references_resource: SingleSheetResource,
) -> Output[OpenTECRReferenceDT]:
    """Define the openTECR references asset."""
    result = OpenTECRReference.validate(references_resource.fetch())
    return Output(
        result,
        metadata={
            **table_metadata(result),
            "source": MetadataValue.url(references_resource.url),
        },
    )


@asset
def opentecr_data(
    data_resource: SingleSheetResource,
) -> Output[OpenTECRDataDT]:
    """Define the openTECR data asset."""
    result = OpenTECRData.validate(data_resource.fetch())
    return Output(
        result,
        metadata={
            **table_metadata(result),
            "source": MetadataValue.url(data_resource.url),
        },
    )


@asset
def opentecr_comments(
    comments_resource: SingleSheetResource,
) -> Output[OpenTECRTableCommentDT]:
    """Define the openTECR comments asset."""
    result = OpenTECRTableComment.validate(comments_resource.fetch())
    return Output(
        result,
        metadata={
            **table_metadata(result),
            "source": MetadataValue.url(comments_resource.url),
        },
    )
