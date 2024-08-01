import pandas as pd
from dagster import MetadataValue, OpExecutionContext, Out, Output, graph, op
from upath import UPath

from data_orchestration.helpers import (
    ValidationModelConfig,
    pandas_metadata,
    validate_pandas_table,
)

from . import types
from .config import GoogleSheetConfig
from .resource import GoogleSheetsResource


@op
def fetch_sheet(
    google_sheets_resource: GoogleSheetsResource,
    config: GoogleSheetConfig,
) -> Output[UPath]:
    """Fetch a Google sheet as Excel file and store it locally."""
    return Output(
        value=google_sheets_resource.fetch(gid=config.gid),
        metadata={
            "source": MetadataValue.url(google_sheets_resource.url(gid=config.gid)),
        },
    )


@op(out=Out(io_manager_key="pandas_io_manager"))
def validate_transform_sheet(
    context: OpExecutionContext,
    config: ValidationModelConfig,
    excel: UPath,
) -> Output[pd.DataFrame]:
    """Validate table contents and return rows conforming with the schema."""
    table = pd.read_excel(excel, engine="openpyxl")

    result = validate_pandas_table(
        table=table,
        model=getattr(types, config.model),
        context=context,
    )

    return Output(
        value=result,
        metadata=pandas_metadata(result),
    )


@graph
def opentecr_table() -> pd.DataFrame:
    """Define the graph of operations to retrieve a table."""
    return validate_transform_sheet(fetch_sheet())
