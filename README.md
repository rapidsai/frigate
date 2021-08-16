# Frigate

Frigate is a tool for automatically generating documentation for your [Helm charts](https://helm.sh/).

<!-- TODO: Add badges for CI, PyPI, etc -->

Features:

- Render documentation from your `Chart.yaml` and `values.yaml` files.
- Supports outputting as markdown, reStructuredText and HTML.
- Sphinx extension for including in Python documentation.

## Installation

```
$ pip install frigate
```

## Usage

```
$ frigate gen path/to/chart

Chart
==========

Chart description.

...
```

<!-- TODO: Link to docs once set up on RTD -->



### Pre-commit-hook

Into the repository you want to have the pre-commit hook installed, run:


```
cat <<EOF >> .pre-commit-config.yaml
- repo: https://github.com/rapidsai/frigate
  rev: v0.4.0 #  pre-commit autoupdate  - to keep the version up to date
  hooks:
    - id: frigate
EOF
```


#### Parameters

You can add extra parameters with :


```
- repo: https://github.com/rapidsai/frigate
  rev: v0.4.0 #  pre-commit autoupdate  - to keep the version up to date
  hooks:
    - id: frigate
      args:
        - --output=README.rst
        - --format=rst
        - --no-credits
        - --no-deps

```