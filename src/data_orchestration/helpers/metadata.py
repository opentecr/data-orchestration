from typing import Any

import pandas as pd
import polars as pl
from dagster import MetadataValue


def pandas_metadata(df: pd.DataFrame) -> dict[str, Any]:
    """Return the metadata of a table."""
    # The conversion to `object` type and `fillna` are workarounds for
    #  https://github.com/astanin/python-tabulate/issues/316.
    return {
        "dagster/row_count": len(df),
        "dagster/column_count": len(df.columns),
        "head": MetadataValue.md(df.head(n=5).astype(object).fillna("").to_markdown()),
        "tail": MetadataValue.md(df.tail(n=5).astype(object).fillna("").to_markdown()),
    }


def polars_metadata(df: pl.DataFrame) -> dict[str, Any]:
    """Return the metadata of a table."""
    # The conversion to `String` type and `fill_null` are workarounds for
    #  https://github.com/astanin/python-tabulate/issues/316.
    with pl.Config(
        tbl_formatting="ASCII_MARKDOWN",
        tbl_hide_column_data_types=True,
        tbl_hide_dataframe_shape=True,
    ):
        return {
            "dagster/row_count": df.height,
            "dagster/column_count": df.width,
            "head": MetadataValue.md(str(df.head(n=5).cast(pl.String).fill_null(""))),
            "tail": MetadataValue.md(str(df.tail(n=5).cast(pl.String).fill_null(""))),
        }
