class CyclicDependencyException(Exception):
    """
    Raised when a cyclic dependency is detected.
    """
    pass


class MissingDependencyException(Exception):
    """
    Raised when a dependency is missing form the input.
    """
    pass
