"""Interface for concrete commands."""
import abc
from dataclasses import dataclass
from typing import Any, Union

from mashumaro.mixins.orjson import DataClassORJSONMixin
from result import Result

from use_case_registry import UseCaseRegistry
from use_case_registry.errors import CommandInputValidationError, UseCaseExecutionError


@dataclass(
    frozen=True,
)
class ICommandInput(DataClassORJSONMixin):
    """ICommandInput."""


class BaseCommand(abc.ABC):
    """Command abstract class."""

    @abc.abstractmethod
    def execute(
        self,
        write_ops_registry: UseCaseRegistry[Any],
    ) -> Result[Any, Union[CommandInputValidationError, UseCaseExecutionError]]:
        """Workflow execution command to complete the use case."""
