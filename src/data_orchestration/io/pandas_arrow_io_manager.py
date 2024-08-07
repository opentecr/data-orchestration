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


"""Provide an I/O manager for pandas DataFrames stored in arrow format."""

from dagster import InputContext, OutputContext, UPathIOManager
from pandas import DataFrame, read_feather
from upath import UPath


class PandasArrowIOManager(UPathIOManager):
    """Define the I/O manager for pandas DataFrames stored in arrow format."""

    extension = ".arrow"

    def dump_to_path(
        self, context: OutputContext, obj: DataFrame, path: UPath
    ) -> None:
        """Store a pandas DataFrame output in an Apache Arrow file."""
        obj.to_feather(path, compression="zstd")

    def load_from_path(self, context: InputContext, path: UPath) -> DataFrame:
        """Load a pandas DataFrame input from an Apache Arrow file."""
        return read_feather(path)
