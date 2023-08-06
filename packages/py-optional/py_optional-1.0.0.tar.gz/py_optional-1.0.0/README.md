# py-optional

<p align="center">
    <em>Optional value implementation for python.</em>
</p>

<p align="center">
<a href="https://github.com/francipvb/py-optional/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/francipvb/py-optional/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://github.com/francipvb/py-optional/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/francipvb/py-optional/workflows/Publish/badge.svg" alt="Publish">
</a>
<a href="https://dependabot.com/" target="_blank">
    <img src="https://flat.badgen.net/dependabot/francipvb/py-optional?icon=dependabot" alt="Dependabot Enabled">
</a>
<a href="https://codecov.io/gh/francipvb/py-optional" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/francipvb/py-optional?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/py-optional" target="_blank">
    <img src="https://img.shields.io/pypi/v/py-optional?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/py-optional/" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/py-optional.svg" alt="Python Versions">
</a>

## Getting started

See [Documentation](https://francipvb.github.io/py-optional/) for details.

## Features

- Poetry (virtual environment and publish to PyPi, all with one tool)
- black (linting/formatter)
- autoflake (removing unused packages)
- isort (dependency organization)
- mypy (static type checking)
- pytest (including test coverage)
- [pre-commit](https://pre-commit.com/) (hooks on commit)
- GitHub Actions for CI/CD
- mkdocs for documentation (with material theme)

## Installing py-optional

Install the latest release:

```bash
pip install py-optional
```

Or you can clone `py-optional` and get started locally

```bash

# ensure you have Poetry installed
pip install --user poetry

# install all dependencies (including dev)
poetry install

# develop!

```

## Example Usage

```python
import py-optional

# do stuff
```

Only **Python 3.8+** is supported as required by the black, pydantic packages

## Publishing to Pypi

### Poetry's documentation

Note that it is recommended to use [API tokens](https://pypi.org/help/#apitoken) when uploading packages to PyPI.

> Once you have created a new token, you can tell Poetry to use it:

<https://python-poetry.org/docs/repositories/#configuring-credentials>

We do this using GitHub Actions' Workflows and Repository Secrets!

### Repo Secrets

Go to your repo settings and add a `PYPI_TOKEN` environment variable:

![Github Actions setup of Poetry token environment variable](images/Github-Secrets-PYPI_TOKEN-Setup.png)

### Inspect the GitHub Actions Publish Workflows

```yml
name: Publish

on:
  release:
    types:
      - created

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      ...
      ...
      ...
      - name: Publish
        env:
          PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
        run: |
          poetry config pypi-token.pypi $PYPI_TOKEN
          bash scripts/publish.sh
```

> That's it!

When you make a release on GitHub, the publish workflow will run and deploy to PyPi! 🚀🎉😎

## Contributing Guide

Welcome! 😊👋

> Please see the [Contributing Guide](https://github.com/francipvb/py-optional/CONTRIBUTING.md).
