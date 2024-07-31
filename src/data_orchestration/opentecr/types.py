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


"""Provide type definitions."""

from typing import ClassVar

import pandera as pa
from dagster_pandera import pandera_schema_to_dagster_type
from pandas import Int64Dtype
from pandera.typing import Series


class BaseModel(pa.DataFrameModel):
    """Define a base model for all dataframe models."""

    class Config:
        """Define the configuration of the base model."""

        strict = "filter"


class OpenTECRUniqueTableKey(BaseModel):
    """Define a unique reference to a table in a publication."""

    part: Series[int] = pa.Field(description="Part of the publication referenced.")
    page: Series[int] = pa.Field(description="Page of the publication referenced.")
    column: Series[int] = pa.Field(
        description="Column on the page (left=1 and right=2).",
        alias="col l/r",
    )
    table_index: Series[int] = pa.Field(
        description="Index of the table on the page starting with 1 from the top.",
        alias="table from top",
    )

    class Config:
        """Configure the reference model."""

        unique: ClassVar[list[str]] = [
            "part",
            "page",
            "col l/r",
            "table from top",
        ]


class OpenTECRTableMetadata(OpenTECRUniqueTableKey):
    """Define the expected shape of the metadata sheet."""

    reaction: Series[str] = pa.Field(
        description="The (possibly corrected) reaction description.",
    )
    reference_code: Series[str] = pa.Field(
        description="Code used to reference the publication source.",
    )
    secondary_comment: Series[str] = pa.Field(
        description="Comment added by secondary curator.",
        alias="curator comment",
        nullable=True,
        coerce=True,
    )
    method: Series[str] = pa.Field(
        description="The experimental methodology used to quantify the apparent "
        "equilibrium constant [K'].",
        nullable=True,
    )
    buffer: Series[str] = pa.Field(
        description="The buffer added to the aqueous solution.",
        nullable=True,
    )


class OpenTECRTableComment(OpenTECRUniqueTableKey):
    """Define the expected shape of the comments sheet."""

    was_spellchecked: Series[Int64Dtype] = pa.Field(
        description="Whether the table comment was manually spellchecked.",
        alias="manually spellchecked",
        nullable=True,
        coerce=True,
    )
    primary_comment: Series[str] = pa.Field(
        description="Comment from the primary curation.",
        alias="comment",
        nullable=True,
    )


class OpenTECRData(BaseModel):
    """Define the expected shape of the data entry sheet."""

    part: Series[Int64Dtype] = pa.Field(
        description="Part of the publication referenced.",
        nullable=True,
        coerce=True,
    )
    page: Series[Int64Dtype] = pa.Field(
        description="Page of the publication referenced.",
        nullable=True,
        coerce=True,
    )
    column: Series[Int64Dtype] = pa.Field(
        description="Column on the page (left=1 and right=2).",
        alias="col l/r",
        nullable=True,
        coerce=True,
    )
    table_index: Series[Int64Dtype] = pa.Field(
        description="Index of the table on the page starting with 1 from the top.",
        alias="table from top",
        nullable=True,
        coerce=True,
    )
    entry_index: Series[str] = pa.Field(
        description="The entry in the table from the top starting at 1. May contain "
        "text comments which indicates rows to drop.",
        alias="entry nr",
        nullable=True,
        coerce=True,
    )
    id: Series[str] = pa.Field(
        description="Unique identifier (W3ID) for the entry, if any.",
        nullable=True,
    )
    temperature: Series[float] = pa.Field(
        description="Temperature of the reaction in Kelvin [K].",
    )
    ionic_strength: Series[float] = pa.Field(
        description="The molar ionic strength of the solution [M].",
        nullable=True,
    )
    hydrogen_potential: Series[float] = pa.Field(
        description="The potential of hydrogen of the solution [pH].",
        alias="p_h",
        nullable=True,
    )
    magnesium_potential: Series[float] = pa.Field(
        description="The potential of magnesium of the solution [pMg].",
        alias="p_mg",
        nullable=True,
    )
    apparent_equilibrium: Series[float] = pa.Field(
        description="The apparent equilibrium constant of the reaction [K'].",
        alias="K_prime",
        nullable=True,
    )
    additional_info: Series[str] = pa.Field(
        description="Additional information provided.",
        nullable=True,
        alias="additional data",
        coerce=True,
    )


class OpenTECRReference(BaseModel):
    """Define the expected shape of the references sheet."""

    reference_code: Series[str] = pa.Field(
        description="Code used to reference the publication source.",
    )
    pmid: Series[str] = pa.Field(
        description="The PubMed identifier (PMID), if any.",
        nullable=True,
        coerce=True,
    )
    doi: Series[str] = pa.Field(
        description="The digital object identifier (DOI), if any.",
        nullable=True,
    )


OpenTECRTableMetadataDT = pandera_schema_to_dagster_type(OpenTECRTableMetadata)
OpenTECRTableCommentDT = pandera_schema_to_dagster_type(OpenTECRTableComment)
OpenTECRDataDT = pandera_schema_to_dagster_type(OpenTECRData)
OpenTECRReferenceDT = pandera_schema_to_dagster_type(OpenTECRReference)
