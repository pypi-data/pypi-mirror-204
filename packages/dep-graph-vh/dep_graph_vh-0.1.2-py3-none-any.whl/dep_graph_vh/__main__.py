"""
Responsible for printing the dependency graph from the default location via:
    `python -m dep_graph_vh`
"""
from dep_graph_vh import resolver
from dep_graph_vh import visualizer

visualizer.print_dep_graph(resolver.get_graph())
