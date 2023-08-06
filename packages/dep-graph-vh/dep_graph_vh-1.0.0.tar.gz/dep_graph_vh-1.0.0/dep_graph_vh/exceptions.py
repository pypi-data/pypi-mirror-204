"""
Exceptions that may be raised during dependency graph resolution.
"""


class CyclicDependencyException(Exception):
    """
    Raised when a cyclic dependency is detected.
    """


class MissingDependencyException(Exception):
    """
    Raised when a dependency is missing form the input.
    """
