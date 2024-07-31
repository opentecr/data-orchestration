import pandas as pd
from dagster import MetadataValue, Out, Output, graph, op

from data_orchestration.helpers import pandas_metadata

from .config import GoogleSheetConfig
from .resource import GoogleSheetsResource


# @op(out=Out(io_manager_key="pandas_io_manager"))
@op
def fetch_sheet(
    google_sheets_resource: GoogleSheetsResource,
    config: GoogleSheetConfig,
) -> Output[pd.DataFrame]:
    """Fetch a Google sheet."""
    result = google_sheets_resource.fetch(gid=config.gid)
    return Output(
        value=result,
        metadata={
            **pandas_metadata(result),
            "source": MetadataValue.url(google_sheets_resource.url(gid=config.gid)),
        },
    )


@graph
def opentecr_table() -> pd.DataFrame:
    """Define the graph of operations to retrieve a table."""
    return fetch_sheet()
