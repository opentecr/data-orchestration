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


"""Provide openTECR bronze layer assets."""

from dagster import graph_asset

from data_orchestration.opentecr.op import opentecr_table
from data_orchestration.opentecr.types import (
    OpenTECRDataDT,
    OpenTECRReferenceDT,
    OpenTECRTableCommentDT,
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
