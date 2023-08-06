"""Target based configuration parser."""
import pathlib
from typing import Any

import jinja2
import yaml
from result import Err, Ok, Result

from use_case_registry.errors import EnvVarMissingError
from use_case_registry.pasers.macros import env_var


class RawConfigParser:
    """Raw config parser."""

    def __init__(
        self,
        path_to_folder: pathlib.Path,
    ) -> None:
        """Raw configuration file parser."""
        self.path_to_folder = path_to_folder

    def parse(self, template: str) -> Result[dict[str, Any], EnvVarMissingError]:
        """Parse file and return especific target config."""
        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=self.path_to_folder,
                followlinks=False,
                encoding="utf-8",
            ),
            autoescape=True,
        )
        try:
            rendered_template = jinja_env.get_template(
                name=template,
                globals={
                    "env_var": env_var,
                },
            ).render()
        except EnvVarMissingError as e:
            return Err(e)
        configuration = yaml.safe_load(stream=rendered_template)

        return Ok(configuration["config"])
