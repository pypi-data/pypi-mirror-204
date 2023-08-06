"""Jinja macros."""
import os
from typing import Optional

from use_case_registry.errors import EnvVarMissingError


def env_var(var: str, default: Optional[str] = None) -> str:
    """
    Return the environment variable named `var`.

    If there is no such environment variable set, return the `default` value.

    If the `default` value is `None`, raise an exception
    """
    if var in os.environ:
        return os.environ[var]

    if default:
        return default
    raise EnvVarMissingError(env_var=var)
