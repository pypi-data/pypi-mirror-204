# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Test the routines that parse various config files."""

from __future__ import annotations

import errno
import pathlib
import tempfile
import typing
from unittest import mock

import pytest

from collect_unexported import defs
from collect_unexported import parse


if typing.TYPE_CHECKING:
    from typing import IO, Any, Final


_FAKE_CONFIG: defs.Config = defs.Config(
    noop=True,
    src=defs.Source(
        top=pathlib.Path("/nonexistent/top"),
        debian=pathlib.Path("/nonexistent/debian"),
        changelog=pathlib.Path("/nonexistent/changelog"),
        package_name="nothing",
        upstream_version="42.616",
    ),
    verbose=True,
)


def test_parse_config_read() -> None:
    """Make sure `parse_config_file()` fails on nonexistent files or read errors."""

    def mock_open_eio(path: pathlib.Path, mode: str) -> IO[bytes]:
        """Mock the `open()` call, do not really return anything."""
        assert path == pathlib.Path(__file__)
        assert mode == "rb"
        raise OSError(errno.EIO, str(path), "oops")

    with pytest.raises(parse.ConfigReadError) as xinfo:
        parse.parse_config_file(_FAKE_CONFIG, pathlib.Path("/nonexistent"))

    assert isinstance(xinfo.value.err, FileNotFoundError)

    with mock.patch("pathlib.Path.open", new=mock_open_eio), pytest.raises(
        parse.ConfigReadError
    ) as xinfo:
        parse.parse_config_file(_FAKE_CONFIG, pathlib.Path(__file__))

    err: Final = xinfo.value
    assert isinstance(err.err, OSError)
    assert err.err.errno == errno.EIO


@pytest.mark.parametrize(
    ("lines", "etype"),
    [
        ([":)"], parse.ConfigParseError),
        ([], parse.ConfigTypeError),
        (["[format.version]", "major = 616"], parse.ConfigTypeError),
        (["[format.version]", "major = 0"], parse.ConfigMissingError),
        (["[format.version]", "major = 0", "[files]"], parse.ConfigMissingError),
        (["[format.version]", "major = 0", "[files]", "include = 616"], parse.ConfigTypeError),
        (["[format.version]", "major = 0", "[files]", 'include = "hello"'], parse.ConfigTypeError),
        (
            ["[format.version]", "major = 0", "[files]", 'include = ["hello", 616]'],
            parse.ConfigTypeError,
        ),
    ],
)
def test_parse_config_format(lines: list[str], etype: type[parse.ConfigError]) -> None:
    """Make sure `parse_config_file()` fails on invalid TOML or bad elements."""
    with tempfile.NamedTemporaryFile(
        prefix="collect-unexported-", suffix=".toml", mode="r+t", encoding="UTF-8"
    ) as tempf:
        print(f"Using {tempf.name} as a temporary file")  # noqa: T201
        print("\n".join(lines), file=tempf)
        tempf.flush()

        with pytest.raises(etype):
            parse.parse_config_file(_FAKE_CONFIG, pathlib.Path(tempf.name))


def test_parse_config_good() -> None:
    """Parse a valid config file."""
    with tempfile.NamedTemporaryFile(
        prefix="collect-unexported-", suffix=".toml", mode="r+t", encoding="UTF-8"
    ) as tempf:
        print(f"Using {tempf.name} as a temporary file")  # noqa: T201
        print(
            """
[format.version]
major = 0
minor = 42

[files]
include = [
  "something",
  "another/thing",
  "and/yet/another/thing",
]
""",
            file=tempf,
        )
        tempf.flush()

        assert parse.parse_config_file(_FAKE_CONFIG, pathlib.Path(tempf.name)) == [
            "something",
            "another/thing",
            "and/yet/another/thing",
        ]


def test_parse_attr_read() -> None:
    """Make sure `get_ignored_files()` fails on nonexistent files or read errors."""

    def mock_open_eio(
        path: pathlib.Path,
        mode: str,
        *,
        encoding: str = "(not specified)",
        **_kwargs: Any,  # noqa: ANN401
    ) -> IO[bytes]:
        """Mock the `open()` call, do not really return anything."""
        assert path == pathlib.Path(__file__)
        assert mode == "r"
        assert encoding == "ISO-8859-15"
        raise OSError(errno.EIO, str(path), "oops")

    with pytest.raises(parse.AttributesReadError) as xinfo:
        parse.get_ignored_files(pathlib.Path("/nonexistent"))

    assert isinstance(xinfo.value.err, FileNotFoundError)

    with mock.patch("pathlib.Path.open", new=mock_open_eio), pytest.raises(
        parse.AttributesReadError
    ) as xinfo:
        parse.get_ignored_files(pathlib.Path(__file__))

    err: Final = xinfo.value
    assert isinstance(err.err, OSError)
    assert err.err.errno == errno.EIO


def test_parse_attr_good() -> None:
    """Make sure `get_ignored_files()` returns the correct value on valid files."""
    with tempfile.NamedTemporaryFile(
        prefix=".gitattributes.", mode="r+t", encoding="UTF-8"
    ) as tempf:
        print(
            """
/tests   export-ignore
test_data	export-ignore -negated and=more
#commented-out export-ignore

src  export-ignore-not-really

bin     eol=none
""",
            file=tempf,
        )
        tempf.flush()

        assert sorted(parse.get_ignored_files(pathlib.Path(tempf.name))) == ["test_data", "tests"]
