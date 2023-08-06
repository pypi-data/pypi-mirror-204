# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Collect some additional files needed for the package build."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile
import typing

import click

from . import defs
from . import examine
from . import gitrepo
from . import parse


if typing.TYPE_CHECKING:
    from typing import Final


@click.command(
    name="collect-unexported", help="Collect some source files not present in the release tarball"
)
@click.option(
    "--config-file",
    "-c",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=pathlib.Path),
    default="collect-unexported.toml",
    help="the path to the TOML config file listing the files to include",
)
@click.option(
    "--noop", "-N", is_flag=True, help="no-operation mode; do not generate the output file"
)
@click.option("--verbose", "-v", is_flag=True, help="verbose operation; display diagnostic output")
def main(*, config_file: pathlib.Path, noop: bool, verbose: bool) -> None:
    """Parse command-line options, check out the repository, collect the files."""
    cfg: Final = defs.Config(noop=noop, src=examine.find_source(), verbose=verbose)
    cfg.diag(lambda: f"Found the top-level source directory at {cfg.src.top}")
    repo_url: Final = examine.get_repo_url(cfg)

    to_include: Final = parse.parse_config_file(cfg, config_file)

    with tempfile.TemporaryDirectory(prefix="collect-unexported.") as tempd_name:
        tempd: Final = pathlib.Path(tempd_name)

        repo: Final = gitrepo.clone_repo(cfg, tempd, repo_url, to_include)
        ufile: Final = gitrepo.build_tarball(cfg, tempd, repo, to_include)

        if cfg.noop:
            subprocess.check_call(["ls", "-l", "--", ufile])
        else:
            target: Final = cfg.src.top.parent / ufile.name
            cfg.diag(lambda: f"Moving the unexported tarball to {target}")
            try:
                ufile.rename(target)
            except OSError as err:
                sys.exit(f"Could not rename {ufile} to {target}: {err}")
