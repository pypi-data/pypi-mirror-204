"""Test enums."""
from use_case_registry.enums import OptionEnums


class _ExampleEnums(OptionEnums):
    A = "A"
    A_B = "A_B"


def test_to_display() -> None:
    """Test to display."""
    assert _ExampleEnums.to_display() == ["a", "a-b"]


def test_from_display() -> None:
    """Test from display."""
    assert _ExampleEnums.from_display(enum_choice="a") is _ExampleEnums.A
