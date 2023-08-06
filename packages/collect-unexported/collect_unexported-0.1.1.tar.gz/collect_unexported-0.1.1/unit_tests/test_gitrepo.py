# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Test the routines that clone and examine a Git repository."""

from __future__ import annotations

import contextlib
import pathlib
import subprocess
import tarfile
import tempfile
import typing

import pytest

from collect_unexported import defs
from collect_unexported import examine
from collect_unexported import gitrepo


if typing.TYPE_CHECKING:
    from typing import Final

pytest.register_assert_rewrite("unit_tests.util")

from unit_tests import util  # noqa: E402  # We want the asserts rewritten


def test_clone() -> None:
    """Test cloning a Git repository."""
    with tempfile.TemporaryDirectory() as tempd_name:
        tempd: Final = pathlib.Path(tempd_name)

        repo_dir: Final = util.setup_git_repo(tempd)
        topdir: Final = util.setup_deb_package(tempd, repo_dir=repo_dir)
        assert not util.is_there(topdir / ".gitattributes")
        subprocess.check_call(["cat", "--", "debian/upstream/metadata"], cwd=topdir)

        with contextlib.chdir(topdir):
            src: Final = examine.find_source()

        cfg: Final = defs.Config(noop=True, src=src, verbose=True)
        repo_url: Final = examine.get_repo_url(cfg)
        print(repo_url)  # noqa: T201
        assert repo_url.endswith(f"//{repo_dir}")

        cloned: Final = gitrepo.clone_repo(cfg, tempd, repo_url, util.TO_INCLUDE)
        assert (cloned / ".gitattributes").is_file()
        assert (cloned / "debian/changelog").is_file()
        assert (cloned / "tests").is_dir()


def test_build() -> None:
    """Test building the final tarball."""
    with tempfile.TemporaryDirectory() as tempd_name:
        tempd: Final = pathlib.Path(tempd_name)
        repo: Final = tempd / "repo"
        repo.mkdir(mode=0o755)

        (repo / "a.txt").write_text("mellon\n", encoding="UTF-8")
        (repo / "b.txt").write_text("xyzzy\n", encoding="UTF-8")
        (repo / "sub").mkdir(mode=0o755)
        (repo / "sub/text.txt").write_text("lurking\n", encoding="UTF-8")

        package_name: Final = "mess"
        upstream_version: Final = "42.616"
        cfg: Final = defs.Config(
            noop=True,
            src=defs.Source(
                top=pathlib.Path("/nonexistent/dir/top"),
                debian=pathlib.Path("/nonexistent/dir/debian"),
                changelog=pathlib.Path("/nonexistent/file/changelog"),
                package_name=package_name,
                upstream_version=upstream_version,
            ),
            verbose=True,
        )
        built: Final = gitrepo.build_tarball(cfg, tempd, repo, ["sub", "b.txt"])
        assert built == tempd / "mess_42.616.orig-unexported.tar.gz"

        members: Final = tarfile.open(built, mode="r:gz").getmembers()
        assert sorted(member.name for member in members if member.isdir()) == [
            "unexported",
            "unexported/sub",
        ]
        assert sorted(member.name for member in members if member.isfile()) == [
            "unexported/b.txt",
            "unexported/sub/text.txt",
        ]
