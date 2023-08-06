<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# Collect files omitted from the release tarballs

\[[Home][ringlet] | [GitLab][gitlab] | [PyPI][pypi]\]

## Overview

Some projects explicitly exclude some development files from
their release tarballs.
Sometimes, when packaging those projects, it may be useful to have
these files around, e.g. for running tests.

The `collect-unexported` utility examines the control files within
a Debian source package, clones its upstream repository, and then
creates an additional source file archive containing some of
the files that have explicitly been omitted from the upstream archive.
This allows a Debian package to e.g. run some source tests that use
scripts and data files that the upstream authors exclude from
the distributed source archive.
The `collect-unexported` tool creates an additional (component) original
tarball (`.orig-unexported.tar.gz`) and places it in the directory where
the Debian packaging tools expect to find the original source tarball
(the `.orig.tar.gz` one).

Please note that the `collect-unexported` tool is limited in
its functionality; it is meant to handle several specific cases, and
it may fail in others.

## Examples

Use the `collect-unexported.toml` file in the current directory,
create an additional source tarball, display some diagnostic information
in the process:

``` sh
collect-unexported -v
```

Use a file with a different name, do not overwrite the source tarball:

``` sh
collect-unexported -c unexported.toml -N
```

## The configuration file

To figure out which files it needs to repack from the upstream repository,
the `collect-unexported` tool reads a TOML file, `collect-unexported.toml`
by default.
That file must currently contain two sections:

- `[format.version]`: a table containing two fields, `major` and `minor`,
  describing the format of the configuration file itself.
  The only version currently supported version is "0.1".
- `[files]`: a table that describes the files that need to be included:
    - `include`: a list of strings, each specifying the relative path from
      the top of the source repository to a single file or directory to be
      included in the component archive

Note that all the paths specified in the `files.include` list must be
excluded in the upstream project's `.gitattributes` file using
the `export-ignore` attribute.

An example configuration file for packing the contents of the `tests` and
`test_data` subdirectories may look like this:

``` toml
[format.version]
major = 0
minor = 1

[files]
include = [
  "test_data",
  "tests",
]
```

## Contact

The `collect-unexported` tool is developed in [a GitLab repository][gitlab]
and is hosted [at Ringlet][ringlet].
A Python package may be downloaded from [the Python package index][pypi].

The author, Peter Pentchev, may be contacted [via e-mail][roam].

[gitlab]: https://gitlab.com/ppentchev/collect-unexported "The collect-unexported GitLab repository"
[ringlet]: https://devel.ringlet.net/misc/collect-unexported/ "The collect-unexported Ringlet home page"
[roam]: mailto:roam@ringlet.net "Peter Pentchev"
[pypi]: https://pypi.org/project/collect-unexported "The collect-unexported PyPI Python package"
