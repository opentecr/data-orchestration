from typing import Annotated

from dagster import Config
from pydantic import Field


class ValidationModelConfig(Config):
    """Configure the name of the model to use for table validation."""

    model: Annotated[
        str, Field(default=..., description="The name of a validation model.")
    ]
