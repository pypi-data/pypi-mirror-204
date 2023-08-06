import dwave_networkx as dnx


def make_chimera_architecture():
    return dnx.chimera_graph(8, 16, 4)
