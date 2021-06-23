[![Build Status][ci-badge]][ci-link]
[![codecov.io][codecov-badge]][codecov-link]
[![PyPI version][pypi-badge]][pypi-link]

# mdformat-myst

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
- [roles](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-roles)
- [inline and block "dollar math"](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#math-shortcuts)
- [comments](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-comments)
- [block breaks](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-blockbreaks)
- [targets](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#syntax-targets)
- [front matter](https://myst-parser.readthedocs.io/en/latest/using/syntax.html#extended-block-tokens)
- [footnotes](https://pandoc.org/MANUAL.html#footnotes)

## Install

```sh
pip install mdformat-myst
```

## Usage

```sh
mdformat <filename>
```

[ci-badge]: https://github.com/executablebooks/mdformat-myst/workflows/Tests/badge.svg?branch=master
[ci-link]: https://github.com/executablebooks/mdformat-myst/actions?query=workflow%3ATest+branch%3Amaster+event%3Apush
[codecov-badge]: https://codecov.io/gh/executablebooks/mdformat-myst/branch/master/graph/badge.svg
[codecov-link]: https://codecov.io/gh/executablebooks/mdformat-myst
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-myst.svg
[pypi-link]: https://pypi.org/project/mdformat-myst
