"""Test schema validator."""
import pytest

from use_case_registry.base.schema_validator import SchemaValidator


class _ASchema(SchemaValidator):
    name: str
    last_name: str


def test_cannot_set_variables() -> None:
    """Test unable to set variables to schema."""
    schema = _ASchema(name="Tomas", last_name="Perez")
    with pytest.raises(TypeError):
        schema.name = "other"
