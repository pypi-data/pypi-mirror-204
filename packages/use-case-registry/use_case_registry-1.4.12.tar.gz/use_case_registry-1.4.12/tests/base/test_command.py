"""Tests for command."""
from dataclasses import dataclass
from typing import Any, Union

import pytest
from pydantic import Field, ValidationError
from result import Err, Ok, Result
from typing_extensions import assert_never

from use_case_registry import UseCaseRegistry
from use_case_registry.base.command import BaseCommand, ICommandInput
from use_case_registry.base.schema_validator import SchemaValidator
from use_case_registry.errors import CommandInputValidationError, UseCaseExecutionError


class ExampleCommandInputSchema(SchemaValidator):
    """Example comamnd schema validator."""

    name: str = Field(min_length=1)
    last_name: str = Field(min_length=1, max_length=10)
    age: int = Field(gt=0)


@dataclass(
    frozen=True,
    repr=False,
    eq=False,
)
class ExampleCommandInput(ICommandInput):
    """Example command input."""

    name: str
    last_name: str
    age: int


class ExampleCommand(BaseCommand):
    """Example command."""

    def __init__(self, inputs: ExampleCommandInput) -> None:
        """Use case constructor."""
        self.inputs = inputs

    def execute(
        self,
        write_ops_registry: UseCaseRegistry[Any],
    ) -> Result[Any, Union[CommandInputValidationError, UseCaseExecutionError]]:
        """Command execution."""
        _ = write_ops_registry

        try:
            ExampleCommandInputSchema(
                name=self.inputs.name,
                last_name=self.inputs.last_name,
                age=self.inputs.age,
            )
        except ValidationError as e:
            return Err(CommandInputValidationError(msg=str(e)))

        return Ok()


def exhaustiveness_checking() -> None:
    """Test exhaustiveness checking."""
    workflow = ExampleCommand(
        inputs=ExampleCommandInput(
            name="Tomas",
            last_name="Perez",
            age=24,
        ),
    )
    workflow_result = workflow.execute(
        write_ops_registry=UseCaseRegistry[Any](max_length=0),
    )
    if not isinstance(workflow_result, Ok):
        workflow_err = workflow_result.err()
        if isinstance(workflow_err, UseCaseExecutionError):  # noqa: SIM114
            assert True
        elif isinstance(workflow_err, CommandInputValidationError):
            assert True
        else:
            assert_never(workflow_err)
    raise AssertionError


@pytest.mark.parametrize(
    argnames="inputs",
    argvalues=[
        ExampleCommandInput(
            name="",
            last_name="",
            age=-1,
        ),
    ],
)
def test_workflow_fails_validation(inputs: ExampleCommandInput) -> None:
    """Test workflow fails do to validation err."""
    workflow_err = (
        ExampleCommand(inputs=inputs)
        .execute(
            write_ops_registry=UseCaseRegistry[Any](
                max_length=0,
            ),
        )
        .err()
    )
    assert isinstance(workflow_err, CommandInputValidationError)
