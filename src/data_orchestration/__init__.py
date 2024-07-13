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

from dagster import Definitions, load_assets_from_modules

from . import assets
from .assets import GoogleSheetsResource, SingleSheetResource

sheets = GoogleSheetsResource(
    spreadsheet_id="1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c",
)

defs = Definitions(
    assets=load_assets_from_modules([assets], group_name="openTECR"),
    resources={
        "metadata_resource": SingleSheetResource(sheets=sheets, gid="652907302"),
        "references_resource": SingleSheetResource(sheets=sheets, gid="81596307"),
        "data_resource": SingleSheetResource(sheets=sheets, gid="2123069643"),
        "comments_resource": SingleSheetResource(sheets=sheets, gid="1475422539"),
    },
)
