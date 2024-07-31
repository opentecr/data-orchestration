
from typing import Annotated

from dagster import Config
from pydantic import Field


class MetaNetXTableConfig(Config):
    """Define a MetaNetX table name resource."""

    table: Annotated[
        str,
        Field(
            default=...,
            description="The MetaNetX table filename, for example, comp_prop.tsv.",
        ),
    ]
