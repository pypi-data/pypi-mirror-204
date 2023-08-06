# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Helper functions for the collect-unexported unit test suite."""

from __future__ import annotations

import pathlib
import subprocess
import typing


if typing.TYPE_CHECKING:
    from typing import Final


PACKAGE_NAME: Final = "frobinator"
UPSTREAM_VERSION: Final = "0.1.0"
DEBIAN_REVISION: Final = "1"
URL_TO_REPLACE: Final = "file:///FIXME"

DATA_BASE: Final = pathlib.Path(__file__).parent.parent / "test_data"
DATA_DIR: Final = DATA_BASE / PACKAGE_NAME

MORE_DIR: Final = DATA_BASE / "unexp"

TO_INCLUDE: Final = ["tests"]


def is_there(path: pathlib.Path) -> bool:
    """Check whether an object "is there" on the filesystem.

    If the object is a symlink, we do not care about its target.
    This function is pretty much only called to make sure that an object
    does *not* exist on the filesystem.
    """
    return path.is_symlink() or path.exists()


def setup_tarball(tempd: pathlib.Path) -> pathlib.Path:
    """Pack up the Debian source package in the `test_data` directory."""
    filename: Final = f"{PACKAGE_NAME}_{UPSTREAM_VERSION}.orig.tar.gz"
    tarball: Final = tempd / filename
    assert not is_there(tarball)
    subprocess.check_call(["tar", "czf", tarball, "-C", DATA_BASE, "--", DATA_DIR.name])
    assert tarball.is_file()
    return tarball


def setup_deb_package(tempd: pathlib.Path, *, repo_dir: pathlib.Path | None = None) -> pathlib.Path:
    """Set up a structure similar to a Debian source package, return the topdir."""
    debdir: Final = tempd / DATA_DIR.name
    assert not is_there(debdir)

    tarball: Final = setup_tarball(tempd)
    assert tarball.parent == tempd
    assert not is_there(debdir)
    subprocess.check_call(["tar", "xaf", tarball.name], cwd=tempd)
    assert debdir.is_dir()

    if repo_dir is not None:
        meta_path: Final = debdir / "debian/upstream/metadata"
        current: Final = meta_path.read_text(encoding="UTF-8")
        updated: Final = current.replace(URL_TO_REPLACE, f"file://{repo_dir}")
        meta_path.write_text(updated, encoding="UTF-8")

    return debdir


def setup_git_repo(tempd: pathlib.Path) -> pathlib.Path:
    """Set up a Git repository containing some additional files."""
    git_top: Final = tempd / "git"
    git_top.mkdir(mode=0o755)
    git_tarball: Final = setup_tarball(git_top)

    subprocess.check_call(["tar", "xaf", git_tarball.name], cwd=git_top)
    repo_dirs: Final = [path for path in git_top.iterdir() if path.is_dir()]
    assert len(repo_dirs) == 1
    repo_dir: Final = repo_dirs[0]
    assert repo_dir.name == DATA_DIR.name
    git_tarball.unlink()

    subprocess.check_call(["git", "init", "-b", "main"], cwd=repo_dir)
    subprocess.check_call(
        ["git", "config", "--local", "user.name", "J. Random Tester"], cwd=repo_dir
    )
    subprocess.check_call(
        ["git", "config", "--local", "user.email", "jrt@example.com"], cwd=repo_dir
    )
    subprocess.check_call(["git", "config", "--local", "commit.gpgSign", "false"], cwd=repo_dir)
    subprocess.check_call(["cat", "--", ".git/config"], cwd=repo_dir)

    subprocess.check_call(["git", "add", "."], cwd=repo_dir)
    subprocess.check_call(["git", "commit", "-m", "The distributed files"], cwd=repo_dir)

    unexp_tarball: Final = repo_dir / "unexp.tar"
    subprocess.check_call(["tar", "cf", unexp_tarball, "."], cwd=MORE_DIR)
    subprocess.check_call(["tar", "xf", unexp_tarball.name], cwd=repo_dir)
    unexp_tarball.unlink()

    subprocess.check_call(["git", "add", "."], cwd=repo_dir)
    subprocess.check_call(["git", "commit", "-m", "The non-exported files"], cwd=repo_dir)

    subprocess.check_call(["git", "tag", "-m", "This is it", "0.1.0"], cwd=repo_dir)

    subprocess.check_call(["git", "rm", "-r", "tests"], cwd=repo_dir)
    subprocess.check_call(
        ["git", "commit", "-m", "This should not interfere with the 0.1.0 tag"], cwd=repo_dir
    )

    return repo_dir
