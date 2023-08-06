"""Test target-based parser."""
import os
import pathlib
from typing import Any
from unittest import mock

import pytest

from use_case_registry.base.schema_validator import SchemaValidator
from use_case_registry.errors import EnvVarMissingError
from use_case_registry.pasers.raw import RawConfigParser


class _Schema(SchemaValidator):
    name: str
    last_name: str


class _OtherSchema(SchemaValidator):
    other: str


class TestTargetBasedConfigParser:  # noqa: D101
    @mock.patch.dict(
        os.environ,
        {},
        clear=True,
    )
    @pytest.mark.parametrize(
        argnames=["template", "expected_result"],
        argvalues=[
            (
                "config-1.yml",
                {
                    "name": "t",
                    "last_name": "p",
                },
            ),
        ],
    )
    def test_parse_works(self, template: str, expected_result: dict[str, Any]) -> None:
        """Test parse works as expected."""
        folder = pathlib.Path().cwd().joinpath("tests/assets/templates/raw/")
        parser = RawConfigParser(path_to_folder=folder)
        result = parser.parse(template=template).unwrap()
        _Schema(**result)
        assert result == expected_result

    @mock.patch.dict(
        os.environ,
        {
            "NAME": "tomas",
            "LAST_NAME": "perez",
        },
        clear=True,
    )
    @pytest.mark.parametrize(
        argnames=["template", "expected_result"],
        argvalues=[
            (
                "config-1.yml",
                {
                    "name": "tomas",
                    "last_name": "perez",
                },
            ),
        ],
    )
    def test_parse_works_using_env_variables(
        self,
        template: str,
        expected_result: dict[str, Any],
    ) -> None:
        """Test parse works as expected."""
        folder = pathlib.Path().cwd().joinpath("tests/assets/templates/raw/")
        parser = RawConfigParser(path_to_folder=folder)
        result = parser.parse(template=template).unwrap()
        _Schema(**result)
        assert result == expected_result

    @pytest.mark.parametrize(
        argnames="template",
        argvalues=[
            "config-2.yml",
        ],
    )
    def test_parse_env_var_missing(
        self,
        template: str,
    ) -> None:
        """Test parse works as expected."""
        folder = pathlib.Path().cwd().joinpath("tests/assets/templates/raw/")
        parser = RawConfigParser(path_to_folder=folder)

        parse_err = parser.parse(template=template).err()

        assert isinstance(parse_err, EnvVarMissingError)
