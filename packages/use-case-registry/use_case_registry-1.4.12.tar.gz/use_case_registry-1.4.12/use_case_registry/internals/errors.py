"""Internal error definitions."""


class UseCaseRagistryEmptyError(Exception):
    """Raised when trying to prune state on an empty registry."""

    def __init__(self) -> None:
        """Construct class."""
        super().__init__("Registry is already empty.")


class UseCaseRegistryLengthExceedError(Exception):
    """Raised when trying to add n+1 items in a n-lenght registry."""

    def __init__(self) -> None:
        """Construct class."""
        super().__init__("Storage exceeded max length configured.")
