"""Provide MetaNetX assets."""

from dagster import graph_asset
from polars import DataFrame

from .op import mnx_table


@graph_asset(
    config={
        "mnx_table": {"ops": {"fetch_table": {"config": {"table": "comp_depr.tsv"}}}},
    },
)
def mnx_comp_depr() -> DataFrame:
    """Define the comp_depr table asset."""
    return mnx_table()


@graph_asset(
    config={
        "mnx_table": {"ops": {"fetch_table": {"config": {"table": "comp_prop.tsv"}}}},
    },
)
def mnx_comp_prop() -> DataFrame:
    """Define the comp_prop table asset."""
    return mnx_table()


@graph_asset(
    config={
        "mnx_table": {"ops": {"fetch_table": {"config": {"table": "comp_xref.tsv"}}}},
    },
)
def mnx_comp_xref() -> DataFrame:
    """Define the comp_xref table asset."""
    return mnx_table()
