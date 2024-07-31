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

from dagster import graph_asset

from .op import opentecr_table
from .types import (
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
                "validate_sheet": {"config": {"model": "OpenTECRTableMetadata"}},
            },
        },
    },
)
def opentecr_metadata() -> OpenTECRTableMetadataDT:
    """Define the openTECR metadata asset."""
    return opentecr_table()


@graph_asset(
    config={
        "opentecr_table": {
            "ops": {
                "fetch_sheet": {"config": {"gid": "81596307"}},
                "validate_sheet": {"config": {"model": "OpenTECRReference"}},
            },
        },
    },
)
def opentecr_references() -> OpenTECRReferenceDT:
    """Define the openTECR references asset."""
    return opentecr_table()


@graph_asset(
    config={
        "opentecr_table": {
            "ops": {
                "fetch_sheet": {"config": {"gid": "2123069643"}},
                "validate_sheet": {"config": {"model": "OpenTECRData"}},
            },
        },
    },
)
def opentecr_data() -> OpenTECRDataDT:
    """Define the openTECR data asset."""
    return opentecr_table()


@graph_asset(
    config={
        "opentecr_table": {
            "ops": {
                "fetch_sheet": {"config": {"gid": "1475422539"}},
                "validate_sheet": {"config": {"model": "OpenTECRTableComment"}},
            },
        },
    },
)
def opentecr_comments() -> OpenTECRTableCommentDT:
    """Define the openTECR comments asset."""
    return opentecr_table()
