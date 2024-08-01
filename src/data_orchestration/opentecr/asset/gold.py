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


"""Provide openTECR gold layer assets."""

from dagster import Output, asset
from pandas import DataFrame

from data_orchestration.helpers import pandas_metadata


@asset(io_manager_key="pandas_io_manager", tags={"layer": "gold"})
def opentecr_denormalized(
    opentecr_clean_data: DataFrame,
    opentecr_table_info: DataFrame,
) -> Output[DataFrame]:
    """Join the openTECR clean data with the table information."""
    result = opentecr_clean_data.join(opentecr_table_info, validate="m:1").set_index(
        "entry_index",
        append=True,
        verify_integrity=True,
    )

    assert len(result) == len(opentecr_clean_data)

    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )
