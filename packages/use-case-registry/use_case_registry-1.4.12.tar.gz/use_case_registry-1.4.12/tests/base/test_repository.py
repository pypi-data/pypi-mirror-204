"""Test for repository."""

from typing import Any

import pytest
from result import Result

from use_case_registry import UseCaseRegistry
from use_case_registry.base.repository import IRepository
from use_case_registry.errors import CommitTransactionsError


class TestICommand:
    """Test definition for ICommand."""

    def test_cannot_be_instantiated(self) -> None:
        """ICommand is an interface an cannot be instantiated."""
        with pytest.raises(TypeError):
            IRepository()  # type:ignore[abstract]

    def test_interface_can_be_extendend(self) -> None:
        """Test interface can be extended."""

        class ConcreteRepository(IRepository):
            def __init__(self) -> None:
                """Construct concrete implementation."""

            def commit_write_transaction(
                self,
                write_operations: UseCaseRegistry[Any],
            ) -> Result[None, CommitTransactionsError]:
                return super().commit_write_transaction(write_operations)

        repo = ConcreteRepository()
        write_registry = UseCaseRegistry[str](
            max_length=10,
        )
        write_registry.add_value(v="Something")

        repo.commit_write_transaction(write_operations=write_registry)
