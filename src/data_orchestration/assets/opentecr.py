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


import pandas as pd
from dagster import asset


@asset
def opentecr_metadata():
    """Define the openTECR metadata asset."""
    return pd.read_excel(
        "https://docs.google.com/spreadsheets/d/1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c/export?gid=652907302&format=xlsx")


@asset
def opentecr_references():
    """Define the openTECR references asset."""
    return pd.read_excel(
        "https://docs.google.com/spreadsheets/d/1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c/export?gid=81596307&format=xlsx")


@asset
def opentecr_data():
    """Define the openTECR data asset."""
    return pd.read_excel(
        "https://docs.google.com/spreadsheets/d/1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c/export?gid=2123069643&format=xlsx")


@asset
def opentecr_comments():
    """Define the openTECR comments asset."""
    return pd.read_excel(
        "https://docs.google.com/spreadsheets/d/1jLIxEXVzE2SAzIB0UxBfcFoHrzjzf9euB6ART2VDE8c/export?gid=1475422539&format=xlsx")
