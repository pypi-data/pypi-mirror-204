# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Test the "look around the Debian source package" functionality."""

from __future__ import annotations

import contextlib
import functools
import pathlib
import tempfile
import typing

import pytest

from collect_unexported import defs
from collect_unexported import examine


if typing.TYPE_CHECKING:
    from typing import Final

pytest.register_assert_rewrite("unit_tests.util")

from unit_tests import util  # noqa: E402  # We want the asserts rewritten


@pytest.mark.parametrize("level", [2, 1, 0, -1])
def test_find_changelog(level: int) -> None:
    """See if we can find the changelog file."""
    with tempfile.TemporaryDirectory() as tempd_name:
        tempd: Final = pathlib.Path(tempd_name)

        if level < 0:
            with contextlib.chdir(tempd):
                with pytest.raises(examine.NoChangelogError) as xinfo:
                    examine.find_source()

                err: Final = xinfo.value
                assert err.cwd == tempd
                assert err.changelog == pathlib.Path("debian/changelog")
                return

        topdir: Final = util.setup_deb_package(tempd)

        def make_next(last: pathlib.Path, level: int) -> pathlib.Path:
            """Make a subdirectory one level in."""
            next_dir: Final = last / f"subdir-{level + 1}"
            next_dir.mkdir(mode=0o755)
            return next_dir

        workdir: Final = functools.reduce(make_next, range(level), topdir)
        with contextlib.chdir(workdir):
            src: Final = examine.find_source()

        assert src == defs.Source(
            top=topdir,
            debian=topdir / "debian",
            changelog=topdir / "debian/changelog",
            package_name=util.PACKAGE_NAME,
            upstream_version=util.UPSTREAM_VERSION,
        )


def test_get_repo_url() -> None:
    """Test the function that parses the URL out of the metadata file."""
    with tempfile.TemporaryDirectory() as tempd_name:
        tempd: Final = pathlib.Path(tempd_name)
        topdir: Final = util.setup_deb_package(tempd)
        with contextlib.chdir(topdir):
            src: Final = examine.find_source()

        cfg: Final = defs.Config(noop=True, src=src, verbose=True)
        repo_url: Final = examine.get_repo_url(cfg)
        assert repo_url == util.URL_TO_REPLACE
