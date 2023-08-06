"""Custom defined errors."""




class CommandInputValidationError(Exception):
    """Raised when command input values does pass validation check."""

    def __init__(self, msg: str) -> None:
        """Construct class."""
        super().__init__(msg)


class UseCaseExecutionError(Exception):
    """Raised when there's an error executing a workflow."""

    def __init__(self, error: Exception) -> None:
        """Construct class."""
        super().__init__(f"{error}")


class CommitTransactionsError(Exception):
    """Raised when there's an error committing a set of transactions."""

    def __init__(self) -> None:
        """Construct class."""
        super().__init__("Error commiting transactions")


class EnvVarMissingError(Exception):
    """Raised when a required enviroment variable is not set."""

    def __init__(self, env_var: str) -> None:
        """Construct class."""
        super().__init__(f"Env var required but not provided {env_var}")


class NotIndentifiedError(Exception):
    """Raised when a not-indetified error happens."""

    def __init__(self, unkown_err: Exception) -> None:  # noqa: D107
        super().__init__(unkown_err)
