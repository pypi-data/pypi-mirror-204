"""Usecase schema validator basemodel."""
import pydantic


class SchemaValidator(pydantic.BaseModel):
    """Base class for schema validators."""

    class Config:
        """Custom configuration."""

        allow_mutation = False
