import polars as pl
from dagster import Out, Output, graph, op
from upath import UPath
from zstandard import ZstdDecompressor

from data_orchestration.helpers import polars_metadata

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


@op(out=Out(io_manager_key="polars_io_manager"))
def load_table(path: UPath) -> Output[pl.DataFrame]:
    """Load a MetaNetX table."""
    with (
        path.open(mode="rb") as handle,
        ZstdDecompressor().stream_reader(handle, closefd=False) as decompressor,
    ):
        try:
            result = pl.read_csv(
                decompressor,
                has_header=False,
                separator="\t",
                comment_prefix="#",
            )
        except pl.exceptions.NoDataError:
            result = pl.DataFrame()
        return Output(value=result, metadata=polars_metadata(result))


@graph
def mnx_table() -> pl.DataFrame:
    """Define the comp_depr table asset."""
    return load_table(fetch_table())
