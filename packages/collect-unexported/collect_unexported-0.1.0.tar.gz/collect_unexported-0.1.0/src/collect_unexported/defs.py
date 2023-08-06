# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Common definitions for the collect-unexported library."""

from __future__ import annotations

import dataclasses
import typing

import cfg_diag


if typing.TYPE_CHECKING:
    import pathlib


VERSION = "0.1.0"
"""The version of the collect-unexported tool."""


@dataclasses.dataclass
class CollectError(Exception):
    """Base class for errors that occur during the collect-unexported operation."""


@dataclasses.dataclass(frozen=True)
class Source:
    """The paths to various files in the examined source tree."""

    top: pathlib.Path
    """The top-level source directory."""

    debian: pathlib.Path
    """The directory containing the Debian packaging files."""

    changelog: pathlib.Path
    """The path to the Debian changelog file."""

    package_name: str
    """The name of the Debian package being processed."""

    upstream_version: str
    """The upstream version of the Debian package being processed."""


@dataclasses.dataclass(frozen=True)
class Config(cfg_diag.Config):
    """Runtime configuration for the collect-unexported tool."""

    noop: bool
    """Do not copy the generated output file out of the temporary directory."""

    src: Source
    """Information about the Debian source package being processed."""
