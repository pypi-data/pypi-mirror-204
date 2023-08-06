# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Test the whole thing."""

from __future__ import annotations

import contextlib
import pathlib
import subprocess
import tempfile
import typing

import pytest
import tomli_w

from collect_unexported import defs
from collect_unexported import examine
from collect_unexported import gitrepo


if typing.TYPE_CHECKING:
    from typing import Final

pytest.register_assert_rewrite("unit_tests.util")

from unit_tests import util  # noqa: E402  # We want the asserts rewritten


def verify_built_tarball(tempd: pathlib.Path, built: pathlib.Path) -> None:
    """Make sure the built tarball contains the correct files."""
    xdir: Final = tempd / "extract"
    xdir.mkdir(mode=0o755)
    subprocess.check_call(["tar", "xaf", built, "-C", xdir])
    subprocess.check_call(["find", "--", xdir, "-ls"])

    unexp: Final = xdir / "unexported"
    assert sorted(path.name for path in unexp.iterdir()) == sorted(util.TO_INCLUDE)
    for subdir in util.TO_INCLUDE:
        subprocess.check_call(["diff", "-qr", "--", unexp / subdir, util.MORE_DIR / subdir])


def test_full() -> None:
    """Test the whole thing: create, examine, clone, build, extract, compare."""
    with tempfile.TemporaryDirectory() as tempd_name:
        tempd: Final = pathlib.Path(tempd_name)

        repo_dir: Final = util.setup_git_repo(tempd)
        topdir: Final = util.setup_deb_package(tempd, repo_dir=repo_dir)

        with contextlib.chdir(topdir):
            src: Final = examine.find_source()

        cfg: Final = defs.Config(noop=True, src=src, verbose=True)
        repo_url: Final = examine.get_repo_url(cfg)
        cloned: Final = gitrepo.clone_repo(cfg, tempd, repo_url, util.TO_INCLUDE)
        built: Final = gitrepo.build_tarball(cfg, tempd, cloned, util.TO_INCLUDE)

        verify_built_tarball(tempd, built)


def test_run() -> None:
    """Test the whole thing, but using the command-line tool."""
    with tempfile.TemporaryDirectory() as tempd_name:
        tempd: Final = pathlib.Path(tempd_name)

        repo_dir: Final = util.setup_git_repo(tempd)
        topdir: Final = util.setup_deb_package(tempd, repo_dir=repo_dir)
        tarball: Final = tempd / f"{util.PACKAGE_NAME}_{util.UPSTREAM_VERSION}.orig.tar.gz"
        assert tarball.is_file()

        assert sorted(path.name for path in tempd.iterdir()) == sorted(
            [
                util.PACKAGE_NAME,
                tarball.name,
                "git",
            ]
        )

        # Ignore the changed repository URL in the metadata file
        subprocess.check_call(["diff", "-qr", "-x", "metadata", "--", topdir, util.DATA_DIR])

        for name in util.TO_INCLUDE:
            assert not util.is_there(topdir / name)

        conffile: Final = tempd / "collect.toml"
        conffile.write_text(
            tomli_w.dumps(
                {
                    "format": {
                        "version": {
                            "major": 0,
                            "minor": 1,
                        },
                    },
                    "files": {
                        "include": util.TO_INCLUDE,
                    },
                }
            ),
            encoding="UTF-8",
        )

        subprocess.check_call(["collect-unexported", "-v", "-c", conffile], cwd=topdir)
        built: Final = tarball.with_name(tarball.name.replace(".orig.", ".orig-unexported."))
        assert built.is_file()
        assert built != tarball

        assert sorted(path.name for path in tempd.iterdir()) == sorted(
            [
                conffile.name,
                util.PACKAGE_NAME,
                tarball.name,
                built.name,
                "git",
            ]
        )

        verify_built_tarball(tempd, built)
