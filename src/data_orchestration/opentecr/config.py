from typing import Annotated

from dagster import Config
from pydantic import Field


class GoogleSheetConfig(Config):
    """Define a single Google sheet resource."""

    gid: Annotated[str, Field(default=..., description="The individual sheet GID.")]


class ValidationModelConfig(Config):
    """Define the pandera model to use for table validation."""

    model: Annotated[
        str, Field(default=..., description="The name of the pandera validation model.")
    ]
