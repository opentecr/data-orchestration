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
from pandas import DataFrame

from .op import opentecr_table
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


# def opentecr_metadata() -> OpenTECRTableMetadataDT:
@graph_asset(
    config={
        "opentecr_table": {"ops": {"fetch_sheet": {"config": {"gid": "652907302"}}}},
    },
)
def opentecr_metadata() -> DataFrame:
    """Define the openTECR metadata asset."""
    # return OpenTECRTableMetadata.validate(opentecr_table())
    return opentecr_table()


# def opentecr_references() -> OpenTECRReferenceDT:
@graph_asset(
    config={
        "opentecr_table": {"ops": {"fetch_sheet": {"config": {"gid": "81596307"}}}},
    },
)
def opentecr_references() -> DataFrame:
    """Define the openTECR references asset."""
    # return OpenTECRReference.validate(opentecr_table())
    return opentecr_table()


# def opentecr_data() -> OpenTECRDataDT:
@graph_asset(
    config={
        "opentecr_table": {"ops": {"fetch_sheet": {"config": {"gid": "2123069643"}}}},
    },
)
def opentecr_data() -> DataFrame:
    """Define the openTECR data asset."""
    # return OpenTECRData.validate(opentecr_table())
    return opentecr_table()


# def opentecr_comments() -> OpenTECRTableCommentDT:
@graph_asset(
    config={
        "opentecr_table": {"ops": {"fetch_sheet": {"config": {"gid": "1475422539"}}}},
    },
)
def opentecr_comments() -> DataFrame:
    """Define the openTECR comments asset."""
    # return OpenTECRTableComment.validate(opentecr_table())
    return opentecr_table()
