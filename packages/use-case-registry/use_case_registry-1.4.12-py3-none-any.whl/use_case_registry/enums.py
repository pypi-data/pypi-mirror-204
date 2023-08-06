"""Custom enums."""

import enum

from typing_extensions import Self


class OptionEnums(str, enum.Enum):
    """Option enums."""

    @classmethod
    def to_display(cls) -> list[str]:
        """Format options enums for pretty display."""

        def _formatter(x: str) -> str:
            return x.lower().replace("_", "-")

        return list(map(_formatter, cls._member_names_))

    @classmethod
    def from_display(cls, enum_choice: str) -> Self:
        """Format back an enum option display input."""
        return cls[enum_choice.replace("-", "_").upper()]
