
from typing import Annotated

from dagster import Config
from pydantic import Field

from data_orchestration.helpers import ValidationModelConfig


class MetaNetXTableConfig(Config):
    """Configure a MetaNetX table file name."""

    table: Annotated[
        str,
        Field(
            default=...,
            description="The MetaNetX table filename, for example, comp_prop.tsv.",
        ),
    ]


class MetaNetXValidationConfig(ValidationModelConfig):
    """Configure a MetaNetX table validation."""

    columns: Annotated[
        list[str],
        Field(
            default=...,
            description="The column headers for the MetaNetX table.",
        ),
    ]
