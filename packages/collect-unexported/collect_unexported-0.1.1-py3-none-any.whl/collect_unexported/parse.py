# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Parse various configuration files related to collect-unexport's work."""

from __future__ import annotations

import dataclasses
import typing

import tomllib

from . import defs


if typing.TYPE_CHECKING:
    import pathlib
    from typing import Any, Final


@dataclasses.dataclass
class ConfigError(defs.CollectError):
    """Base class for errors related to configuration file parsing."""

    config_file: pathlib.Path
    """The path to the config file we tried to process."""


@dataclasses.dataclass
class ConfigReadError(ConfigError):
    """An error that occurred while reading the config file."""

    err: Exception
    """The error that we encountered."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"Could not read the {self.config_file} file: {self.err}"


@dataclasses.dataclass
class ConfigParseError(ConfigError):
    """An error that occurred while parsing the config file."""

    err: Exception
    """The error that we encountered."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"Could not parse the {self.config_file} file: {self.err}"


@dataclasses.dataclass
class ConfigContentsError(ConfigError):
    """Something in the config file was not as we expected it to be."""

    contents: Any
    """The contents of the config file."""

    path: str
    """The path to the element that was not as it should be."""


@dataclasses.dataclass
class ConfigMissingError(ConfigContentsError):
    """An element was not found at all in the config file."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"No '{self.path}' element in the {self.config_file} file"


@dataclasses.dataclass
class ConfigTypeError(ConfigContentsError):
    """An element was not of the correct type."""

    expected: str
    """What the element should have been."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"The '{self.path}' element in the {self.config_file} file is not {self.expected}"


@dataclasses.dataclass
class AttributesError(defs.CollectError):
    """Base class for errors related to .gitattributes parsing."""

    attr_path: pathlib.Path
    """The path to the .gitattributes file we tried to process."""


@dataclasses.dataclass
class AttributesReadError(AttributesError):
    """An error that occurred while reading the .gitattributes file."""

    err: Exception
    """The error that we encountered."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"Could not read the {self.attr_path} file: {self.err}"


@dataclasses.dataclass
class AttributesParseError(AttributesError):
    """An error that occurred while parsing the .gitattributes file."""

    err: Exception
    """The error that we encountered."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"Could not parse the {self.attr_path} file: {self.err}"


def parse_config_file(cfg: defs.Config, config_file: pathlib.Path) -> list[str]:
    """Parse the list of paths to include from the TOML config file."""
    cfg.diag(lambda: f"Reading the collect-unexported configuration from {config_file}")
    try:
        cdata: Final = tomllib.load(config_file.open(mode="rb"))
    except OSError as err:
        raise ConfigReadError(config_file=config_file, err=err) from err
    except ValueError as err:
        raise ConfigParseError(config_file=config_file, err=err) from err
    if (
        not isinstance(cdata, dict)
        or not isinstance(cdata.get("format"), dict)
        or not isinstance(cdata["format"].get("version"), dict)
        or not isinstance(cdata["format"]["version"].get("major"), int)
        or cdata["format"]["version"]["major"] != 0
    ):
        raise ConfigTypeError(
            config_file=config_file, contents=cdata, path="format.version.major", expected="0"
        )

    files: Final = cdata.get("files")
    if not isinstance(files, dict):
        raise ConfigMissingError(config_file=config_file, contents=cdata, path="files")
    lines: Final = files.get("include")
    if lines is None:
        raise ConfigMissingError(config_file=config_file, contents=cdata, path="files.include")
    if not isinstance(lines, list) or any(not isinstance(item, str) for item in lines):
        raise ConfigTypeError(
            config_file=config_file,
            contents=cdata,
            path="files.include",
            expected="a list of strings",
        )
    return lines


def _is_ignored(parts: list[str]) -> str | None:
    """Naively check whether a .gitattributes line specifies a path to skip when exporting."""
    if len(parts) <= 1 or "export-ignore" not in parts[1:]:
        return None

    return parts[0].lstrip("/")


def get_ignored_files(attr_path: pathlib.Path) -> list[str]:
    """Parse a .gitattributes file, return the ignored patterns."""
    try:
        lines: Final = [
            line
            for line in (
                raw.strip() for raw in attr_path.read_text(encoding="ISO-8859-15").splitlines()
            )
            if line and not line.startswith("#")
        ]
    except OSError as err:
        raise AttributesReadError(attr_path=attr_path, err=err) from err
    except ValueError as err:
        raise AttributesParseError(attr_path=attr_path, err=err) from err
    return [
        relpath
        for relpath in (_is_ignored(parts) for parts in (line.split() for line in lines))
        if relpath is not None
    ]
