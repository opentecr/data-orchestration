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


"""Provide openTECR silver layer assets."""

from hashlib import blake2b

from dagster import Output, asset
from pandas import DataFrame

from data_orchestration.helpers import pandas_metadata
from data_orchestration.opentecr.helpers import transform_compound_name
from data_orchestration.opentecr.types import (
    OpenTECRData,
    OpenTECRDataDT,
    OpenTECRReferenceDT,
    OpenTECRTableComment,
    OpenTECRTableCommentDT,
    OpenTECRTableMetadata,
    OpenTECRTableMetadataDT,
)


@asset(io_manager_key="pandas_io_manager", tags={"layer": "silver"})
def opentecr_clean_comments(
    opentecr_table_comments: OpenTECRTableCommentDT,
) -> Output[DataFrame]:
    """Clean the openTECR table comments."""
    result = (
        opentecr_table_comments.rename(
            columns={
                OpenTECRTableComment.column: "column",
                OpenTECRTableComment.table_index: "table_index",
                OpenTECRTableComment.was_spellchecked: "was_spellchecked",
            },
        )
        .assign(
            was_spellchecked=lambda df: df["was_spellchecked"].fillna(0).astype(bool),
            comment=lambda df: df["comment"].str.replace("-", ""),
        )
        .set_index(["part", "page", "column", "table_index"], verify_integrity=True)
    )
    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )


@asset(io_manager_key="pandas_io_manager", tags={"layer": "silver"})
def opentecr_clean_metadata(
    opentecr_table_metadata: OpenTECRTableMetadataDT,
) -> Output[DataFrame]:
    """Clean the openTECR table metadata."""
    result = (
        opentecr_table_metadata.rename(
            columns={
                OpenTECRTableMetadata.column: "column",
                OpenTECRTableMetadata.table_index: "table_index",
                OpenTECRTableMetadata.secondary_comment: "secondary_comment",
            },
        )
        .assign(
            method=lambda df: df["method"].str.replace("-", ""),
            buffer=lambda df: df["buffer"].str.replace("-", "").str.replace("none", ""),
            reaction=lambda df: df["reaction"].str.strip(),
            # TODO: Remove '1' from secondary_comment column.
        )
        .set_index(["part", "page", "column", "table_index"], verify_integrity=True)
    )
    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )


@asset(io_manager_key="pandas_io_manager", tags={"layer": "silver"})
def opentecr_table_info(
    opentecr_clean_comments: DataFrame,
    opentecr_clean_metadata: DataFrame,
    opentecr_references: OpenTECRReferenceDT,
) -> Output[DataFrame]:
    """Join the openTECR table comments and metadata with the references."""
    primary = opentecr_clean_comments.join(opentecr_clean_metadata, validate="1:1")

    # We expect that there is a 1:1 relationship and the number of rows is stable.
    assert len(primary) == len(opentecr_clean_comments) == len(opentecr_clean_metadata)

    result = primary.merge(
        opentecr_references,
        how="left",
        on="reference_code",
        validate="m:1",
    )

    assert len(result) == len(primary)

    result.index = primary.index

    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )


@asset(io_manager_key="pandas_io_manager", tags={"layer": "silver"})
def opentecr_clean_data(
    opentecr_data: OpenTECRDataDT,
) -> Output[DataFrame]:
    """Clean the openTECR data."""
    result = (
        opentecr_data.rename(
            columns={
                OpenTECRData.hydrogen_potential: "hydrogen_potential",
                OpenTECRData.magnesium_potential: "magnesium_potential",
                OpenTECRData.apparent_equilibrium: "apparent_equilibrium",
                OpenTECRData.column: "column",
                OpenTECRData.table_index: "table_index",
                OpenTECRData.entry_index: "entry_index",
                OpenTECRData.additional_info: "additional_info",
            },
        )
        .pipe(
            # Drop rows with 'duplicate' or 'error' in the entry_index column.
            lambda df: df.drop(
                index=df.loc[df["entry_index"].isin(["duplicate", "error"])].index,
            ),
        )
        .assign(
            entry_index=lambda df: df["entry_index"].astype(int),
        )
        .set_index(["part", "page", "column", "table_index"])
    )
    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )


@asset(io_manager_key="pandas_io_manager", tags={"layer": "silver"})
def opentecr_unique_reactions(opentecr_clean_metadata: DataFrame) -> Output[DataFrame]:
    """Extract the reactions from the openTECR table metadata."""
    result = (
        opentecr_clean_metadata.loc[:, ["reaction"]]
        .drop_duplicates(subset="reaction", ignore_index=True)
        .assign(
            reaction_hash=lambda df: df["reaction"]
            .map(
                lambda rxn: blake2b(rxn.encode(), digest_size=20).hexdigest(),
            )
            .reset_index(drop=True),
        )
    )
    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )


@asset(io_manager_key="pandas_io_manager", tags={"layer": "silver"})
def opentecr_compounds(opentecr_unique_reactions: DataFrame) -> Output[DataFrame]:
    """Extract individual compounds from the unique reactions."""
    # Split reaction equations into reactants and products.
    compounds = (
        opentecr_unique_reactions["reaction"]
        .str.split(
            "=",
            n=1,
            expand=True,
            regex=False,
        )
        .rename(columns={0: "reactants", 1: "products"})
    )

    result = (
        opentecr_unique_reactions.loc[:, ["reaction_hash"]]
        # Split the reactants and products into individual compounds.
        .assign(
            reaction_hash=lambda df: df["reaction_hash"].astype("category"),
            reactant=compounds["reactants"].map(
                lambda lhs: [
                    transform_compound_name(name) for name in lhs.split(" + ")
                ],
                na_action="ignore",
            ),
            product=compounds["products"].map(
                lambda rhs: [
                    transform_compound_name(name) for name in rhs.split(" + ")
                ],
                na_action="ignore",
            ),
        )
        # Use the reactant and product columns as a new variable column 'reaction_side'
        # and insert their respective elements into a new value column 'compound'.
        .melt(
            id_vars=["reaction_hash"],
            value_vars=["reactant", "product"],
            var_name="reaction_side",
            value_name="compound",
        )
        .assign(reaction_side=lambda df: df["reaction_side"].astype("category"))
        # Spread the compounds lists to separate rows.
        .explode("compound", ignore_index=True)
        .assign(compound=lambda df: df["compound"].astype("category"))
        # Sort in descending order such that reactants appear before products.
        .sort_values(
            by=["reaction_hash", "reaction_side"], ascending=False, ignore_index=True
        )
    )

    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )
