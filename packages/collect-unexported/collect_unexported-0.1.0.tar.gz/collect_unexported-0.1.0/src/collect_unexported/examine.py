# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Look around the Debian source package directory."""

from __future__ import annotations

import dataclasses
import pathlib
import typing
from urllib import parse as uparse

import yaml
from debian import changelog as dchangelog

from . import defs


if typing.TYPE_CHECKING:
    from typing import Any, Final


CHANGELOG_REL = pathlib.Path("debian/changelog")
"""The relative path of the changelog file to look for."""


@dataclasses.dataclass
class DebianChangelogError(defs.CollectError):
    """Base class for errors related to parsing the debian/changelog file."""

    changelog: pathlib.Path
    """The relative path to the changelog file that we were looking for."""


@dataclasses.dataclass
class NoChangelogError(DebianChangelogError):
    """Could not find the debian/changelog file."""

    cwd: pathlib.Path
    """The directory where we started looking."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"Could not find {self.changelog} in {self.cwd} or any of its parent directories"


@dataclasses.dataclass
class ChangelogReadError(DebianChangelogError):
    """Could not read the debian/changelog file."""

    err: Exception
    """The error that occurred."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"Could not read the {self.changelog} file: {self.err}"


@dataclasses.dataclass
class ChangelogParseError(DebianChangelogError):
    """Could not parse the debian/changelog file."""

    err: Exception
    """The error that occurred."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"Could not parse the {self.changelog} file: {self.err}"


@dataclasses.dataclass
class MetaError(defs.CollectError):
    """Base class for errors related to parsing the debian/upstream/metadata file."""

    meta_path: pathlib.Path
    """The path to the upstream metadata file."""


@dataclasses.dataclass
class MetaReadError(MetaError):
    """Could not read the upstream metadata file."""

    err: Exception
    """The error that occurred."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"Could not read the {self.meta_path} file: {self.err}"


@dataclasses.dataclass
class MetaParseError(MetaError):
    """Could not parse the upstream metadata file."""

    err: Exception
    """The error that occurred."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"Could not parse the {self.meta_path} file: {self.err}"


@dataclasses.dataclass
class MetaContentsError(MetaError):
    """Base class for errors related to the parsed YAML contents."""

    meta: Any
    """The parsed contents of the Debian upstream metadata file."""

    yaml_path: str
    """The "path" to the YAML element that is not as it ought to be."""


@dataclasses.dataclass
class MetaMissingError(MetaContentsError):
    """There is no element at all."""

    def __str__(self) -> str:
        """Report the missing element in a human-readable way."""
        return f"No '{self.yaml_path}' element in the {self.meta_path} file"


@dataclasses.dataclass
class MetaTypeError(MetaContentsError):
    """The element is not of the expected type."""

    expected: str
    """The type we expected the element to be."""

    def __str__(self) -> str:
        """Report the missing element in a human-readable way."""
        return (
            f"The '{self.yaml_path}' element in the {self.meta_path} file is not "
            f"a YAML {self.expected}"
        )


@dataclasses.dataclass
class MetaBadRepositoryError(MetaContentsError):
    """The repository URL in the upstream metadata file could not be parsed."""

    url: str
    """The URL string extracted from the metadata file."""

    err: Exception
    """The error that occurred while trying to parse the URL string."""

    def __str__(self) -> str:
        """Report the bad URL in a human-readable way."""
        return (
            f"The repository URL specified in '{self.yaml_path}' in "
            f"the {self.meta_path} file - '{self.url}' - could not be parsed: {self.err}"
        )


def find_source() -> defs.Source:
    """Look for a `debian/changelog` file higher and higher up."""
    cwd: Final = pathlib.Path(".").resolve()
    try:
        changelog: Final = next(
            cfile
            for cfile in (cdir / CHANGELOG_REL for cdir in [cwd, *cwd.parents])
            if cfile.is_file()
        )
    except StopIteration as err:
        raise NoChangelogError(cwd=cwd, changelog=CHANGELOG_REL) from err

    try:
        chlog_data: Final = dchangelog.Changelog(file=changelog.open(mode="r", encoding="UTF-8"))
    except OSError as err:
        raise ChangelogReadError(changelog=changelog, err=err) from err
    except ValueError as err:
        raise ChangelogParseError(changelog=changelog, err=err) from err

    return defs.Source(
        top=changelog.parent.parent,
        debian=changelog.parent,
        changelog=changelog,
        package_name=chlog_data.package,
        upstream_version=chlog_data.version.upstream_version,
    )


def get_repo_url(cfg: defs.Config) -> str:
    """Grab the repository URL out of the Debian upstream metadata file."""
    meta_path: Final = cfg.src.debian / "upstream/metadata"
    try:
        meta: Final = yaml.safe_load(meta_path.open(mode="rb"))
    except OSError as err:
        raise MetaReadError(meta_path=meta_path, err=err) from err
    except ValueError as err:
        raise MetaParseError(meta_path=meta_path, err=err) from err
    if not isinstance(meta, dict):
        raise MetaTypeError(meta_path=meta_path, meta=meta, yaml_path=".", expected="object")

    url_string: Final = meta.get("Repository")
    if url_string is None:
        raise MetaMissingError(meta_path=meta_path, meta=meta, yaml_path="Repository")
    if not isinstance(url_string, str):
        raise MetaTypeError(
            meta_path=meta_path, meta=meta, yaml_path="Repository", expected="string"
        )

    # Somewhat canonicalize the URL by making a round trip
    try:
        return uparse.urlparse(url_string).geturl()
    except ValueError as err:
        raise MetaBadRepositoryError(
            meta_path=meta_path, meta=meta, yaml_path="Repository", url=url_string, err=err
        ) from err
