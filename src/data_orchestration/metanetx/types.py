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

import pandera as pa
from dagster_pandera import pandera_schema_to_dagster_type
from pandas import Int64Dtype
from pandera.typing import Series


class BaseModel(pa.DataFrameModel):
    """Define a base model for all dataframe models."""

    class Config:
        """Configure the base model."""

        strict = True
        ordered = True


class MetaNetXDeprecation(BaseModel):
    """Define the shape of the deprecation table."""

    deprecated_id: Series[str] = pa.Field(
        description="The deprecated identifier [MNX_ID]."
    )
    replacement_id: Series[str] = pa.Field(
        description="The replacement identifier [MNX_ID]."
    )
    version: Series[str] = pa.Field(
        description="MNXref version when the identifier was deprecated [STRING]."
    )


class MetaNetXCrossReference(BaseModel):
    """Define the shape of the cross-references table."""

    external_id: Series[str] = pa.Field(
        description="The external identifier [XREF]."
    )
    mnx_id: Series[str] = pa.Field(
        description="The corresponding identifier in the MNXref namespace [MNX_ID]."
    )
    description: Series[str] = pa.Field(
        description="The description given by the external resource [STRING]."
    )


class MetaNetXChemicalProperty(BaseModel):
    """Define the shape of the chemical property table."""

    mnx_id: Series[str] = pa.Field(
        description="The identifier of the chemical compound in the MNXref namespace [MNX_ID]."
    )
    name: Series[str] = pa.Field(
        description="The common name of the compound [STRING]."
    )
    reference: Series[str] = pa.Field(
        description="The reference compound, i.e., a compound selected in an external resource that best represents this entry [REFERENCE]."
    )
    formula: Series[str] = pa.Field(
        description="The formula of the compound [STRING].",
        nullable=True,
    )
    charge: Series[Int64Dtype] = pa.Field(
        description="The charge of the compound [INTEGER].",
        nullable=True,
        coerce=True,
    )
    mass: Series[float] = pa.Field(
        description="The mass of the compound [REAL].",
        nullable=True,
    )
    inchi: Series[str] = pa.Field(
        description="The standard InChI of the compound [STRING].",
        nullable=True,
    )
    inchi_key: Series[str] = pa.Field(
        description="The standard InChIKey of the compound [STRING].",
        nullable=True,
    )
    smiles: Series[str] = pa.Field(
        description="The SMILES representation of the compound [STRING].",
        nullable=True,
    )


class MetaNetXStereochemistry(BaseModel):
    """Define the shape of the stereochemistry table."""

    parent_id: Series[str] = pa.Field(
        description="The parent identifier [MNX_ID]."
    )
    child_id: Series[str] = pa.Field(
        description="The child identifier [MNX_ID]."
    )
    relation: Series[str] = pa.Field(
        description="The relation description [STRING]."
    )


class MetaNetXCompartmentProperty(BaseModel):
    """Define the shape of the compartment property table."""

    mnx_id: Series[str] = pa.Field(
        description="The identifier of the sub-cellular compartment in the MNXref namespace [MNX_ID]."
    )
    name: Series[str] = pa.Field(
        description="The common name of the compartment [STRING]."
    )
    reference: Series[str] = pa.Field(
        description="The compartment in an external resource that best represents this entry [REFERENCE]."
    )


class MetaNetXReactionProperty(BaseModel):
    """Define the shape of the reaction property table."""

    mnx_id: Series[str] = pa.Field(
        description="The identifier of the reaction in the MNXref namespace [MNX_ID]."
    )
    equation: Series[str] = pa.Field(
        description="The equation of the reaction in the MNXref namespace (compartmentalized and undirected) [EQUA]."
    )
    reference: Series[str] = pa.Field(
        description="The original best resource from where this reaction comes from [REFERENCE]."
    )
    ec_number: Series[str] = pa.Field(
        description="The EC number(s) associated with this reaction [STRING].",
        nullable=True,
    )
    is_balanced: Series[bool] = pa.Field(
        description="Whether the equation is balanced with respect to elemental composition and charge [BOOLEAN].",
        coerce=True,
    )
    is_transport: Series[bool] = pa.Field(
        description="Whether this is a transport reaction [BOOLEAN].",
        coerce=True,
    )
