"""
This module contains the logic for resolving parsed dependencies from reader.py
and constructing the fully resolved dependency graph.
Additional checks are performed to ensure that the dependency graph is valid:
    - No cyclic dependencies
    - No missing packages

:raises CyclicDependencyException: when a cyclic dependencies have been found
:raises MissingDependencyException: when a package is missing from the dep_dict
"""
from typing import List, Dict, Set

from . import reader
from .exceptions import CyclicDependencyException, MissingDependencyException


class DependencyGraph:  # pylint: disable=too-few-public-methods
    """
    A class that represents a fully resolved dependency graph.
    It consists of a dictionary of packages and their corresponding resolved dependency graphs.
    """""
    resolved_dependencies: Dict[str, 'DependencyGraph']

    def __init__(self):
        self.resolved_dependencies = {}


def resolve_dfs(packages: List[str],
                visited: Set[str],
                dep_dict: Dict[str, List[str]]) -> DependencyGraph:
    """
    A recursive function that resolves a dependency graph using depth-first search approach.
    It keeps track of the visited nodes in order to spot the cyclic dependencies.
    It verifies that all packages (including the ones with empty dependencies list)
    are present in the dep_dict

    :param packages: list of packages to be resolved and added into the resolved_dependencies dict
    :param visited: set of packages that the current recursion stack have already visited
    :param dep_dict: dictionary of packages and their corresponding dependencies
    :raises CyclicDependencyException: when a cyclic dependencies have been found
    :raises MissingDependencyException: when a package is missing from the dep_dict
    :return: fully resolved dependency graph
    """
    graph = DependencyGraph()
    for package in packages:
        if package in visited:
            raise CyclicDependencyException(
                f'Cycle in dependencies has been detected when processing "{package}" package')
        if package not in dep_dict:
            raise MissingDependencyException(f'Missing "{package}" package from the input json')
        visited.add(package)
        graph.resolved_dependencies[package] = resolve_dfs(dep_dict[package], visited, dep_dict)
        visited.remove(package)
    return graph


def resolve_dependencies(dep_dict: Dict[str, List[str]]) -> DependencyGraph:
    """
    Fully resolve dependency graph based on the provided dictionary of packages
    and their corresponding dependencies.
    Will raise exceptions in case of cyclic dependencies or missing packages

    :param dep_dict: dictionary of packages and their corresponding dependencies
    :return: fully resolved dependency graph object
    """
    packages = list(dep_dict.keys())
    return resolve_dfs(packages, set(), dep_dict)


def get_graph(path: str = reader.get_default_file_path()) -> DependencyGraph:
    """
    Constructs a fully resolved dependency graph object based on the provided path
    to the input json file. If path parameter is not specified,
    use the system-specific default path ("/tmp/deps.json" or "C:\\tmp\\deps.json")

    :param path: optional location of the input json file
    :return: fully resolved graph object
    """
    deps = reader.read_dependencies(path)
    return resolve_dependencies(deps)
