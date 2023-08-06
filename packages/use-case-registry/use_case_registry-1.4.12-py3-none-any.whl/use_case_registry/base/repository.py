"""Interface for concrete repository."""

import abc
from typing import Any

from result import Ok, Result

from use_case_registry import UseCaseRegistry
from use_case_registry.errors import CommitTransactionsError


class IRepository(abc.ABC):
    """Repository gives access to all the system layer."""

    @abc.abstractmethod
    def commit_write_transaction(
        self,
        write_operations: UseCaseRegistry[Any],
    ) -> Result[None, CommitTransactionsError]:
        """Commit a set of write operations as a transaction."""
        write_operations.prune_state()
        return Ok()
