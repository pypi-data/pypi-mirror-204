"""
Test cases for the resolver module.
"""
import os
from unittest import TestCase

from dep_graph_vh import resolver
from dep_graph_vh import visualizer
from dep_graph_vh.exceptions import CyclicDependencyException, MissingDependencyException

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


class TestResolver(TestCase):  # pylint: disable=missing-class-docstring
    def test_resolving_valid_graph(self):
        """
        Test if the graph is resolved correctly.
        """
        valid_graph_path = os.path.join(CURRENT_DIR, 'test_data', 'valid_graph.json')
        converted_string_path = os.path.join(CURRENT_DIR, 'test_data', 'valid_graph_printed.txt')
        with open(converted_string_path, encoding='utf8') as file:
            correct_string = file.read()

        graph = resolver.get_graph(valid_graph_path)

        self.assertTrue(graph)
        self.assertTrue(isinstance(graph, resolver.DependencyGraph))
        deps = graph.resolved_dependencies
        self.assertEqual(len(deps), 3)

        converted = visualizer.convert_dep_graph_to_string(graph)
        self.assertEqual(converted, correct_string)

    def test_resolving_graph_with_cyclic_deps(self):
        """
        Test if the CyclicDependencyException is raised when input contain cyclic dependencies
        """
        graph_with_cyclic_deps_path = os.path.join(
            CURRENT_DIR, 'test_data', 'graph_with_cyclic_deps.json')

        with self.assertRaises(CyclicDependencyException):
            resolver.get_graph(graph_with_cyclic_deps_path)

    def test_resolving_graph_with_missing_deps(self):
        """
        Test if the MissingDependencyException is raised when input has missing dependencies
        """
        graph_with_cyclic_deps_path = os.path.join(
            CURRENT_DIR, 'test_data', 'graph_with_missing_deps.json')

        with self.assertRaises(MissingDependencyException):
            resolver.get_graph(graph_with_cyclic_deps_path)
