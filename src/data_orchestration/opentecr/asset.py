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

from dagster import Output, asset, graph_asset
from pandas import DataFrame

from data_orchestration.helpers import pandas_metadata

from .op import opentecr_table
from .types import (
    OpenTECRData,
    OpenTECRDataDT,
    OpenTECRReferenceDT,
    OpenTECRTableComment,
    OpenTECRTableCommentDT,
    OpenTECRTableMetadata,
    OpenTECRTableMetadataDT,
)


@graph_asset(
    config={
        "opentecr_table": {
            "ops": {
                "fetch_sheet": {"config": {"gid": "652907302"}},
                "validate_transform_sheet": {
                    "config": {"model": "OpenTECRTableMetadata"},
                },
            },
        },
    },
    tags={"layer": "bronze"},
)
def opentecr_table_metadata() -> OpenTECRTableMetadataDT:
    """Define the openTECR table metadata asset."""
    return opentecr_table()


@graph_asset(
    config={
        "opentecr_table": {
            "ops": {
                "fetch_sheet": {"config": {"gid": "81596307"}},
                "validate_transform_sheet": {"config": {"model": "OpenTECRReference"}},
            },
        },
    },
    tags={"layer": "bronze"},
)
def opentecr_references() -> OpenTECRReferenceDT:
    """Define the openTECR references asset."""
    return opentecr_table()


@graph_asset(
    config={
        "opentecr_table": {
            "ops": {
                "fetch_sheet": {"config": {"gid": "2123069643"}},
                "validate_transform_sheet": {"config": {"model": "OpenTECRData"}},
            },
        },
    },
    tags={"layer": "bronze"},
)
def opentecr_data() -> OpenTECRDataDT:
    """Define the openTECR data asset."""
    return opentecr_table()


@graph_asset(
    config={
        "opentecr_table": {
            "ops": {
                "fetch_sheet": {"config": {"gid": "1475422539"}},
                "validate_transform_sheet": {
                    "config": {"model": "OpenTECRTableComment"},
                },
            },
        },
    },
    tags={"layer": "bronze"},
)
def opentecr_table_comments() -> OpenTECRTableCommentDT:
    """Define the openTECR table comments asset."""
    return opentecr_table()


@asset(tags={"layer": "silver"})
def opentecr_clean_comments(
    opentecr_table_comments: OpenTECRTableCommentDT,
) -> Output[DataFrame]:
    """Clean the openTECR table comments."""
    result = (
        opentecr_table_comments.rename(
            columns={
                OpenTECRTableComment.column: "column",
                OpenTECRTableComment.table_index: "table_index",
                OpenTECRTableComment.was_spellchecked: "was_spellchecked",
            },
        )
        .assign(
            was_spellchecked=lambda df: df["was_spellchecked"].fillna(0).astype(bool),
            comment=lambda df: df["comment"].str.replace("-", ""),
        )
        .set_index(["part", "page", "column", "table_index"], verify_integrity=True)
    )
    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )


@asset(tags={"layer": "silver"})
def opentecr_clean_metadata(
    opentecr_table_metadata: OpenTECRTableMetadataDT,
) -> Output[DataFrame]:
    """Clean the openTECR table metadata."""
    result = (
        opentecr_table_metadata.rename(
            columns={
                OpenTECRTableMetadata.column: "column",
                OpenTECRTableMetadata.table_index: "table_index",
                OpenTECRTableMetadata.secondary_comment: "secondary_comment",
            },
        )
        .assign(
            method=lambda df: df["method"].str.replace("-", ""),
            buffer=lambda df: df["buffer"].str.replace("-", "").str.replace("none", ""),
            # TODO: Remove '1' from secondary_comment column.
        )
        .set_index(["part", "page", "column", "table_index"], verify_integrity=True)
    )
    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )


@asset(tags={"layer": "silver"})
def opentecr_table_info(
    opentecr_clean_comments: DataFrame,
    opentecr_clean_metadata: DataFrame,
    opentecr_references: OpenTECRReferenceDT,
) -> Output[DataFrame]:
    """Join the openTECR table comments and metadata with the references."""
    primary = opentecr_clean_comments.join(opentecr_clean_metadata, validate="1:1")

    # We expect that there is a 1:1 relationship and the number of rows is stable.
    assert len(primary) == len(opentecr_clean_comments) == len(opentecr_clean_metadata)

    result = primary.merge(
        opentecr_references,
        how="left",
        on="reference_code",
        validate="m:1",
    )

    assert len(result) == len(primary)

    result.index = primary.index

    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )


@asset(tags={"layer": "silver"})
def opentecr_clean_data(
    opentecr_data: OpenTECRDataDT,
) -> Output[DataFrame]:
    """Clean the openTECR data."""
    result = (
        opentecr_data.rename(
            columns={
                OpenTECRData.hydrogen_potential: "hydrogen_potential",
                OpenTECRData.magnesium_potential: "magnesium_potential",
                OpenTECRData.apparent_equilibrium: "apparent_equilibrium",
                OpenTECRData.column: "column",
                OpenTECRData.table_index: "table_index",
                OpenTECRData.entry_index: "entry_index",
                OpenTECRData.additional_info: "additional_info",
            },
        )
        .pipe(
            # Drop rows with 'duplicate' or 'error' in the entry_index column.
            lambda df: df.drop(
                index=df.loc[df["entry_index"].isin(["duplicate", "error"])].index,
            ),
        )
        .assign(
            entry_index=lambda df: df["entry_index"].astype(int),
        )
        .set_index(["part", "page", "column", "table_index"])
    )
    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )


@asset(tags={"layer": "gold"})
def opentecr_denormalized(
    opentecr_clean_data: DataFrame,
    opentecr_table_info: DataFrame,
) -> Output[DataFrame]:
    """Join the openTECR clean data with the table information."""
    result = opentecr_clean_data.join(opentecr_table_info, validate="m:1").set_index(
        "entry_index", append=True, verify_integrity=True,
    )

    assert len(result) == len(opentecr_clean_data)

    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )
