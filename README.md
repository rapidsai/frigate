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
