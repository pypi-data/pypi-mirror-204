"""
This module contains the functions to convert the dependency graph to string representation
and print it to the sdtout.
"""
from typing import List

from .resolver import DependencyGraph

PADDING = '  '


def convert_with_padding(graph: DependencyGraph, level: int = 0) -> List[str]:
    """
    Convert recursively the dependency graph with the added level of padding

    :param graph: the dependency graph to be converted
    :param level: the level of the graph. Used to add the padding.
    :return: string list representing graph with added padding
    """
    res = []
    for package, dep_graph in graph.resolved_dependencies.items():
        res.append(f'{PADDING * level}- {package}')
        res += convert_with_padding(dep_graph, level + 1)
    return res


def convert_dep_graph_to_string(graph: DependencyGraph) -> str:
    """
    Convert the dependency graph to string representation

    :param graph: the dependency graph to be converted
    :return: string representation of the provided graph
    """
    return '\n'.join(convert_with_padding(graph, 0))


def print_dep_graph(graph: DependencyGraph) -> None:
    """
    Print the dependency graph to sdtout

    :param graph: the dependency graph to be printed
    :return: None
    """
    print(convert_dep_graph_to_string(graph))
