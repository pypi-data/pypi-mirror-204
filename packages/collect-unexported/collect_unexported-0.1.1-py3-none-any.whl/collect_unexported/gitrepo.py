# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Clone, examine, and extract files out of a Git repository."""

from __future__ import annotations

import dataclasses
import subprocess
import typing

from . import defs
from . import parse


if typing.TYPE_CHECKING:
    import pathlib
    from typing import Final


@dataclasses.dataclass
class RepoError(defs.CollectError):
    """Base class for errors that occurred while handling the Git repository."""

    repo_url: str
    """The upstream repository URL."""

    err: Exception
    """The error that occurred while switching to the Git tag."""


@dataclasses.dataclass
class RepoCloneError(RepoError):
    """Could not clone the Git repository."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"Could not clone the {self.repo_url} repository: {self.err}"


@dataclasses.dataclass
class RepoTagError(RepoError):
    """Could not switch to the Git tag corresponding to the upstream version."""

    tag: str
    """The Git tag that we tried to switch to."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"Could not switch to the '{self.tag}' Git tag: {self.err}"


@dataclasses.dataclass
class RepoNonIgnoredError(defs.CollectError):
    """Some of the files to repack are not actually ignored."""

    repo_url: str
    """The upstream repository URL."""

    ignored: list[str]
    """The files that were specified as ignored in the .gitattributes file."""

    missing: list[str]
    """The files that were specified for inclusion, but are not ignored."""

    def __str__(self) -> str:
        """Complain in a human-readable manner."""
        return f"Non-ignored files specified for inclusion: {self.missing!r}"


@dataclasses.dataclass
class RenameError(defs.CollectError):
    """Could not rename a file."""

    source: pathlib.Path
    """The file we tried to rename."""

    target: pathlib.Path
    """What we tried to rename it to."""

    err: Exception
    """The error we encountered."""

    def __str__(self) -> str:
        """Report the failure in a human-readable manner."""
        return f"Could not rename {self.source} to {self.target}: {self.err}"


def clone_repo(
    cfg: defs.Config, tempd: pathlib.Path, repo_url: str, to_include: list[str]
) -> pathlib.Path:
    """Clone the upstream Git repository, validate the list of files to include."""
    repo: Final = tempd / "repo"

    cfg.diag(lambda: f"Cloning {repo_url} into {repo}")
    try:
        subprocess.check_call(["git", "clone", "--", repo_url, repo])
    except (subprocess.CalledProcessError, OSError) as err:
        raise RepoCloneError(repo_url=repo_url, err=err) from err

    git_tag: Final = cfg.src.upstream_version
    cfg.diag(lambda: f"Checking out the '{git_tag}' tag")
    try:
        subprocess.check_call(["git", "checkout", f"refs/tags/{git_tag}"], cwd=repo)
    except (subprocess.CalledProcessError, OSError) as err:
        raise RepoTagError(repo_url=repo_url, tag=git_tag, err=err) from err

    ignored: Final = parse.get_ignored_files(repo / ".gitattributes")
    missing: Final = [name for name in to_include if name not in ignored]
    if missing:
        raise RepoNonIgnoredError(repo_url=repo_url, ignored=ignored, missing=missing)

    return repo


def build_tarball(
    cfg: defs.Config, tempd: pathlib.Path, repo: pathlib.Path, to_include: list[str]
) -> pathlib.Path:
    """Collect the files to include again into an 'unexported' tarball."""
    cfg.diag(lambda: f"Collecting {len(to_include)} path(s) into the 'unexported' tarball")
    udir: Final = tempd / "unexported"
    udir.mkdir(mode=0o755)
    for name in to_include:
        try:
            (repo / name).rename(udir / name)
        except OSError as err:
            raise RenameError(source=repo / name, target=udir / name, err=err) from err

    ufile: Final = (
        tempd / f"{cfg.src.package_name}_{cfg.src.upstream_version}.orig-{udir.name}.tar.gz"
    )
    subprocess.check_call(
        ["tar", "-cf", ufile.name.removesuffix(".gz"), "--", udir.name],
        cwd=tempd,
    )
    subprocess.check_call(["gzip", "-9", "-n", "--", ufile.name.removesuffix(".gz")], cwd=tempd)

    return ufile
