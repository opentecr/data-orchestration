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


"""Provide top level symbols."""

import os

from dagster import Definitions, load_assets_from_modules
from upath import UPath

from .opentecr import asset as opentecr_assets
from .opentecr.resource import GoogleSheetsResource
from .io import PandasArrowIOManager, PolarsArrowIOManager
from .metanetx.resource import MetaNetXResource
from .metanetx import asset as metanetx_assets

defs = Definitions(
    assets=[
        *load_assets_from_modules([opentecr_assets], group_name="openTECR"),
        *load_assets_from_modules([metanetx_assets], group_name="MetaNetX"),
    ],
    resources={
        "google_sheets_resource": GoogleSheetsResource(
            spreadsheet_id="1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c",
        ),
        "metanetx_resource": MetaNetXResource(
            base_path=str(UPath(os.getenv("DAGSTER_HOME", ".")) / "storage"),
        ),
        "pandas_io_manager": PandasArrowIOManager(
            base_path=UPath(os.getenv("DAGSTER_HOME", ".")) / "storage",
        ),
        "polars_io_manager": PolarsArrowIOManager(
            base_path=UPath(os.getenv("DAGSTER_HOME", ".")) / "storage",
        ),
    },
)
