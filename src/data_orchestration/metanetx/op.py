import pandas as pd
import polars as pl
from dagster import OpExecutionContext, Out, Output, graph, op
from upath import UPath
from zstandard import ZstdDecompressor

from data_orchestration.helpers import (
    ValidationModelConfig,
    pandas_metadata,
    validate_pandas_table,
)

from . import types
from .config import MetaNetXTableConfig
from .resource import MetaNetXResource


@op
def fetch_table(
    metanetx_resource: MetaNetXResource,
    config: MetaNetXTableConfig,
) -> Output[UPath]:
    """Fetch a MetaNetX table."""
    return Output(
        value=metanetx_resource.fetch(table=config.table),
        metadata={"source": metanetx_resource.url(table=config.table)},
    )


@op(out=Out(io_manager_key="pandas_io_manager"))
def etl_table(
    context: OpExecutionContext,
    config: ValidationModelConfig,
    path: UPath,
) -> Output[pd.DataFrame]:
    """ETL a MetaNetX table."""
    with (
        path.open(mode="rb") as handle,
        ZstdDecompressor().stream_reader(handle, closefd=False) as decompressor,
    ):
        try:
            table = pl.read_csv(
                decompressor,
                has_header=False,
                separator="\t",
                comment_prefix="#",
            ).to_pandas()
        except pl.exceptions.NoDataError:
            table = pd.DataFrame()
    # TODO: Set column names from config.

    result = validate_pandas_table(
        table=table,
        model=getattr(types, config.model),
        context=context,
    )

    return Output(value=result, metadata=pandas_metadata(result))


@graph
def mnx_table() -> pd.DataFrame:
    """Define the graph of operations for loading a MetaNetX table."""
    return etl_table(fetch_table())
