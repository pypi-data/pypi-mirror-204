"""
Test for the visualizer module.
"""
from unittest import TestCase

from dep_graph_vh import visualizer
from dep_graph_vh.resolver import DependencyGraph


class TestVisualizer(TestCase):  # pylint: disable=missing-class-docstring
    @staticmethod
    def build_valid_test_graph() -> DependencyGraph:
        """
        Build a valid graph for testing purposes.

        {
          "pkg1": {"pkg2": {}, "pkg3": {}},
          "pkg2": {},
          "pkg3": {}
        }

        :return: The test graph object.
        """
        graph = DependencyGraph()

        graph1 = DependencyGraph()
        graph1.resolved_dependencies['pkg2'] = DependencyGraph()
        graph1.resolved_dependencies['pkg3'] = DependencyGraph()

        graph.resolved_dependencies['pkg3'] = DependencyGraph()
        graph.resolved_dependencies['pkg2'] = DependencyGraph()
        graph.resolved_dependencies['pkg1'] = graph1
        return graph

    @staticmethod
    def get_valid_test_graph_str_representation() -> str:
        """
        Provide correct string representation for graph:

        {
          "pkg1": {"pkg2": {}, "pkg3": {}},
          "pkg2": {},
          "pkg3": {}
        }

        :return: Correct test graph string representation.
        """
        return '- pkg3\n' \
               '- pkg2\n' \
               '- pkg1\n' \
               '  - pkg2\n' \
               '  - pkg3'

    def test_convert_dep_graph_to_string(self):
        """
        Test the correct conversion of the dependency graph to string.
        """
        graph = TestVisualizer.build_valid_test_graph()

        converted = visualizer.convert_dep_graph_to_string(graph)
        correct_string = TestVisualizer.get_valid_test_graph_str_representation()
        self.assertEqual(converted, correct_string)
