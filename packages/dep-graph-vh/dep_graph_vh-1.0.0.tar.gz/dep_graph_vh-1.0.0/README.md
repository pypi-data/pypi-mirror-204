# Simple dependency graph resolver

## Description

This is a simple graph dependency resolver.
It can parse dependencies in json files from the provided or default system-specific location
(`/tmp/deps.json` or `C:\tmp\deps.json`).
Parsed dependencies can be transformed into a fully resolved dedicated `DependencyGraph` object
that later may be converted into a string representation.

## Installation

```
pip install dep_graph_vh
```

## Usage

#### Print graph from default location:

```
python -m dep_graph_vh
```

#### Obtain a fully resolved dependency graph object from the provided or default location:

```python
import dep_graph_vh as dg

dg.get_graph(file_location)  # from specific location
dg.get_graph()  # from default system-dependent
```

#### Print dependency graph object:

```python
import dep_graph_vh as dg

graph = dg.get_graph()
dg.print_dep_graph(graph)
```

## Development

```
git clone https://gitlab.com/hyhyniak.victor/dep_graph.git
cd dep_graph
pip install -e .

pip install -r dev_requirements.txt
```

## Tests and Quality Assurance

```
python -m unittest

mypy .

pylint dep_graph_vh test

```

## Build, deploy to PyPI and GitLab release

Will be done as part of the CI pipeline after (and only after) new tag creation:

1) Bump up the library version in `pyproject.toml`
2) create a new tag (e.g. `3.0.1`)
