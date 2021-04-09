[![Build Status](https://github.com/hukkinj1/mdformat-myst/workflows/Tests/badge.svg?branch=master)](https://github.com/hukkinj1/mdformat-myst/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)
[![PyPI version](https://img.shields.io/pypi/v/mdformat-myst)](https://pypi.org/project/mdformat-myst)

# mdformat-myst \[IN DEVELOPMENT\]

> Mdformat plugin for MyST compatibility

## Description

[Mdformat](https://github.com/executablebooks/mdformat) is a formatter for
[CommonMark](https://spec.commonmark.org/current/)
compliant Markdown.

Mdformat-myst is an mdformat plugin that changes the target specification to
[MyST](https://myst-parser.readthedocs.io/en/latest/using/syntax.html),
making the tool able to format the following syntax extensions:

- [tables](https://github.github.com/gfm/#tables-extension-)
- [directives](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-directives)
  (No special handling is implemented currently.
  Directives are parsed as if they were code fences,
  and their content is left unchanged.)
- [roles](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-roles)
- TODO: Add the rest

## Install

```sh
pip install mdformat-myst
```

## Usage

```sh
mdformat <filename>
```
