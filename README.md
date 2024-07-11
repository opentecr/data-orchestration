# Data Orchestration

| |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|---|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Package | [![Latest PyPI Version](https://img.shields.io/pypi/v/data-orchestration.svg)](https://pypi.org/project/data-orchestration/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/data-orchestration.svg)](https://pypi.org/project/data-orchestration/) [![Documentation](https://readthedocs.org/projects/data-orchestration/badge/?version=latest)](https://data-orchestration.readthedocs.io/en/latest/?badge=latest)                     |
| Meta | [![Apache-2.0](https://img.shields.io/pypi/l/data-orchestration.svg)](LICENSE) [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](.github/CODE_OF_CONDUCT.md) [![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/) [![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)                                                                     |
| Automation | [![GitHub Workflow](https://github.com/opentecr/data-orchestration/workflows/CI-CD/badge.svg)](https://github.com/opentecr/data-orchestration/workflows/CI-CD) [![Code Coverage](https://codecov.io/gh/opentecr/data-orchestration/branch/master/graph/badge.svg)](https://codecov.io/gh/opentecr/data-orchestration) |

Transform and enrich the raw, curated openTECR data to produce suitable output formats.

## Post Template-Instantiation Steps

1. Start working with git.

    ```shell
    git init
    ```

2. Install the git pre-commit hooks using the `pre-commit` tool.

    ```shell
    pip install pre-commit
    pre-commit install
    ```

3. Commit all the files.

    ```shell
    git add .
    git commit -m "chore: initialize project cookiecutter"
    ```

4. Create a repository on [GitHub](https://github.com) if you haven't done
   so yet.
5. Browse through the architecture decision records (`docs/adr`) if you want
   to understand details of the package design.
6. Remove this section from the readme and describe what your package is all
   about.
7. When you're ready to make a release, perform the following steps.

   1. On [GitHub](https://github.com) set the secure environment
      variables `PYPI_USERNAME` and `PYPI_PASSWORD` to `__token__` and a respective PyPI API token.
   2. Tag your latest commit with the desired version and let GitHub handle
      the release.

        ```shell
        git tag 0.1.0
        git push origin 0.1.0
        ```

## Copyright

* Copyright © 2024 openTECR Community.
* Free software distributed under the [Apache Software License 2.0](../LICENSE).

