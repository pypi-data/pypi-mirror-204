<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# The collect\_unexported Python library

## Common configuration settings and definitions

### Constants

::: collect_unexported.defs.VERSION

### Runtime configuration settings

::: collect_unexported.defs.Source

::: collect_unexported.defs.Config

### Exceptions

::: collect_unexported.defs.CollectError

## Examine the Debian source package structure

### Constants

::: collect_unexported.examine.CHANGELOG_REL

### Functions

::: collect_unexported.examine.find_source

::: collect_unexported.examine.get_repo_url

### Exceptions

::: collect_unexported.examine.DebianChangelogError

::: collect_unexported.examine.NoChangelogError

::: collect_unexported.examine.ChangelogParseError

::: collect_unexported.examine.MetaError

::: collect_unexported.examine.MetaReadError

::: collect_unexported.examine.MetaParseError

::: collect_unexported.examine.MetaContentsError

::: collect_unexported.examine.MetaBadRepositoryError

::: collect_unexported.examine.MetaMissingError

::: collect_unexported.examine.MetaTypeError

## Clone a Git repository, examine its files

### Functions

::: collect_unexported.gitrepo.build_tarball

::: collect_unexported.gitrepo.clone_repo

### Exceptions

::: collect_unexported.gitrepo.RepoError

::: collect_unexported.gitrepo.RepoCloneError

::: collect_unexported.gitrepo.RepoTagError

::: collect_unexported.gitrepo.RepoNonIgnoredError

::: collect_unexported.gitrepo.RenameError

## Parse some configuration files

### Functions

::: collect_unexported.parse.parse_config_file

::: collect_unexported.parse.get_ignored_files

### Exceptions

::: collect_unexported.parse.ConfigError

::: collect_unexported.parse.ConfigContentsError

::: collect_unexported.parse.ConfigReadError

::: collect_unexported.parse.ConfigMissingError

::: collect_unexported.parse.ConfigParseError

::: collect_unexported.parse.ConfigTypeError

::: collect_unexported.parse.AttributesError

::: collect_unexported.parse.AttributesReadError

::: collect_unexported.parse.AttributesParseError
