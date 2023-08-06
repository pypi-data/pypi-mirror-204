"""
Test cases for the reader module
"""
import os
from unittest import TestCase

from dep_graph_vh import reader

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


class TestReader(TestCase):  # pylint: disable=missing-class-docstring
    def test_read_dependencies_from_valid_path(self):
        """
        Test if the dependencies are read and parsed correctly from the valid path.
        """
        valid_path = os.path.join(CURRENT_DIR, 'test_data', 'valid_graph.json')

        deps = reader.read_dependencies(valid_path)
        self.assertTrue(deps)
        self.assertTrue(isinstance(deps, dict))
        self.assertEqual(len(deps), 3)

    def test_read_dependencies_from_invalid_path(self):
        """
        Test if FileNotFoundError is raised when the file is not found in the given path.
        """
        invalid_path = os.path.join(CURRENT_DIR, 'non_existing.json')

        with self.assertRaises(FileNotFoundError):
            reader.read_dependencies(invalid_path)
