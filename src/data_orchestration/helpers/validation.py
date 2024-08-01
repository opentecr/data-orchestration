import json

import pandas as pd
import pandera as pa
from dagster import OpExecutionContext


def validate_pandas_table(
    table: pd.DataFrame,
    model: type[pa.DataFrameModel],
    context: OpExecutionContext,
) -> pd.DataFrame:
    """Validate a pandas DataFrame against a pandera model."""
    try:
        result = model.validate(table, lazy=True)
    except pa.errors.SchemaErrors as exc:
        context.log.error(  # noqa: TRY400
            "Schema errors:\n\n%s",
            json.dumps(exc.message, indent=2),
        )
        context.log.error(  # noqa: TRY400
            "Offending rows:\n\n%s",
            exc.data,
        )
        result = table.loc[~table.index.isin(exc.data.index), :].copy()

    return result
