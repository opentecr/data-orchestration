"""Provide MetaNetX assets."""

from dagster import graph_asset
from pandas import DataFrame

from .op import mnx_table


@graph_asset(
    config={
        "mnx_table": {
            "ops": {
                "fetch_table": {"config": {"table": "comp_depr.tsv"}},
                "etl_table": {"config": {"model": "MetaNetXDeprecation"}},
            },
        },
    },
    tags={"layer": "bronze"},
)
def mnx_comp_depr() -> DataFrame:
    """Define the deprecated compartment identifiers asset."""
    return mnx_table()


@graph_asset(
    config={
        "mnx_table": {
            "ops": {
                "fetch_table": {"config": {"table": "comp_prop.tsv"}},
                "etl_table": {"config": {"model": "MetaNetXCompartmentProperty"}},
            },
        },
    },
    tags={"layer": "bronze"},
)
def mnx_comp_prop() -> DataFrame:
    """Define the compartment properties asset."""
    return mnx_table()


@graph_asset(
    config={
        "mnx_table": {
            "ops": {
                "fetch_table": {"config": {"table": "comp_xref.tsv"}},
                "etl_table": {"config": {"model": "MetaNetXCrossReference"}},
            },
        },
    },
    tags={"layer": "bronze"},
)
def mnx_comp_xref() -> DataFrame:
    """Define the compartment cross-references asset."""
    return mnx_table()


@graph_asset(
    config={
        "mnx_table": {
            "ops": {
                "fetch_table": {"config": {"table": "chem_depr.tsv"}},
                "etl_table": {"config": {"model": "MetaNetXDeprecation"}},
            },
        },
    },
    tags={"layer": "bronze"},
)
def mnx_chem_depr() -> DataFrame:
    """Define the deprecated chemical identifiers asset."""
    return mnx_table()


@graph_asset(
    config={
        "mnx_table": {
            "ops": {
                "fetch_table": {"config": {"table": "chem_isom.tsv"}},
                "etl_table": {"config": {"model": "MetaNetXStereochemistry"}},
            },
        },
    },
    tags={"layer": "bronze"},
)
def mnx_chem_isom() -> DataFrame:
    """Define the stereochemistry asset."""
    return mnx_table()


@graph_asset(
    config={
        "mnx_table": {
            "ops": {
                "fetch_table": {"config": {"table": "chem_prop.tsv"}},
                "etl_table": {"config": {"model": "MetaNetXChemicalProperty"}},
            },
        },
    },
    tags={"layer": "bronze"},
)
def mnx_chem_prop() -> DataFrame:
    """Define the chemical properties asset."""
    return mnx_table()


@graph_asset(
    config={
        "mnx_table": {
            "ops": {
                "fetch_table": {"config": {"table": "chem_xref.tsv"}},
                "etl_table": {"config": {"model": "MetaNetXCrossReference"}},
            },
        },
    },
    tags={"layer": "bronze"},
)
def mnx_chem_xref() -> DataFrame:
    """Define the chemical cross-references asset."""
    return mnx_table()


@graph_asset(
    config={
        "mnx_table": {
            "ops": {
                "fetch_table": {"config": {"table": "reac_depr.tsv"}},
                "etl_table": {"config": {"model": "MetaNetXDeprecation"}},
            },
        },
    },
    tags={"layer": "bronze"},
)
def mnx_reac_depr() -> DataFrame:
    """Define the deprecated reaction identifiers asset."""
    return mnx_table()


@graph_asset(
    config={
        "mnx_table": {
            "ops": {
                "fetch_table": {"config": {"table": "reac_prop.tsv"}},
                "etl_table": {"config": {"model": "MetaNetXReactionProperty"}},
            }
        },
    },
    tags={"layer": "bronze"},
)
def mnx_reac_prop() -> DataFrame:
    """Define the reaction properties asset."""
    return mnx_table()


@graph_asset(
    config={
        "mnx_table": {
            "ops": {
                "fetch_table": {"config": {"table": "reac_xref.tsv"}},
                "etl_table": {"config": {"model": "MetaNetXCrossReference"}},
            }
        },
    },
    tags={"layer": "bronze"},
)
def mnx_reac_xref() -> DataFrame:
    """Define the reaction cross-references asset."""
    return mnx_table()
