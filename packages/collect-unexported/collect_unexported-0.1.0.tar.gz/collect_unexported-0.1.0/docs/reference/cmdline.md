<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

<!--
This file was initially generated from the mdoc manual page
(the src/collect_unexported/collect-unexported.1 file in the source tree)
using the mandoc(1) tool's Markdown output, and then massaged by hand.
-->

# collect-unexported - selectively collect files omitted from release archives

## NAME

**collect-unexported** - selectively collect files omitted from release archives

## SYNOPSIS

**collect-unexported**
\[**-N**&nbsp;|&nbsp;**--noop**]
\[**-v**&nbsp;|&nbsp;**--verbose**]
\[**-c**&nbsp;*configfile*&nbsp;|&nbsp;**--config-file**&nbsp;*configfile*]

**collect-unexported**
**---help**

## DESCRIPTION

The
**collect-unexported**
utility examines the control files within a Debian source package,
clones its upstream repository, and then creates an additional
source file archive containing some of the files that have
explicitly been omitted from the upstream archive.
This allows a Debian package to e.g. run some source tests that use
scripts and data files that the upstream authors exclude from
the distributed source archive.
The
**collect-unexported**
tool creates an additional (component) original tarball
(*.orig-unexported.tar.gz*)
and places it in the directory where the Debian packaging tools
expect to find the original source tarball
(the
*.orig.tar.gz*
one).

Please note that the
**collect-unexported**
tool is limited in its functionality; it is meant to handle several
specific cases, and it may fail in others.

The
**collect-unexported**
utility accepts the following command-line options:

- **-c** *configfile* | **--config-file** *configfile*<br/>
Specify the path to a configuration file
(*collect-unexported.toml by default*)
that defines the list of files and directories to package up.
- **--help**<br/>
Display program usage information and exit.
- **-N** | **--noop**<br/>
No-operation mode - do most of the work, but after creating
the new component archive, do not copy it out of the temporary
directory into the actual distribution directory.
- **-v** | **--verbose**<br/>
Verbose mode - display information about the actions performed.

## ENVIRONMENT

The operation of the
**collect-unexported**
utility is not directly influenced by any environment variables.

## THE CONFIGURATION FILE

The
**collect-unexported**
utility expects to find a single file in TOML format with
the following structure:

- **\[format.version\]**<br/>
  A table describing the structure of the configuration file itself in
  the form of a version string.
  The versioning of the configuration file is loosely based on
  the Semantic Versioning specification: the minor version number is increased
  when new fields or sections are added, while the major version number is
  increased when fields or sections are removed or their types or
  allowed values are changed.
    - **major**<br/>
      The major number of the version format string.
      The
      **collect-unexported**
      tool will refuse to process files for which this value is
      different from 0.
    - **minor**<br/>
      The minor number of the version format string.
- **\[files\]**<br/>
  A table describing the files to fetch from the upstream repository.
    - **include**<br/>
      A list of strings, each specifying the relative path from the top of
      the source repository to a single file or directory to be included in
      the component archive.

## DEBIAN SOURCE PACKAGE FILES

The
**collect-unexported**
utility expects to be run from within an unpacked Debian source package.
Thus, it expects that either the current working directory or one of
its parent directories will contain a subdirectory named
*debian*;
it will then examine the following files within that subdirectory:

- *changelog*
> The
> **collect-unexported**
> tool will extract the source package name and the upstream version from
> the latest Debian changelog entry.
> That information is used to check out the correct Git tag from
> the upstream source repository, and then to create the additional
> source tarball with the correct name and upstream version.
- *upstream/metadata*
> The
> **collect-unexported**
> tool will use the contents of the
> *Repository*
> field to locate the upstream Git repository.

## EXAMPLES

Use the
*collect-unexported.toml*
file in the current directory, create an additional source tarball,
display some diagnostic information in the process:

``` sh
collect-unexported -v
```

Use a file with a different name, do not overwrite the source tarball:

``` sh
collect-unexported -c unexported.toml -N
```

## DIAGNOSTICS

The **collect-unexported** utility exits&#160;0 on success, and&#160;&gt;0 if an error occurs.

## SEE ALSO

dpkg-source(1),
git(1),
deb-changelog(5)

## STANDARDS

No standards were harmed during the production of the
**collect-unexported**
utility.

## HISTORY

The
**collect-unexported**
utility was written by Peter Pentchev in 2023.

## AUTHORS

Peter Pentchev
&lt;roam@ringlet.net&gt;

## BUGS

No, thank you :)
But if you should actually find any, please report them
to the author.
