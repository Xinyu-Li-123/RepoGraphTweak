import networkx as nx
import os

from repograph.Constructor import load_graph_from_path

def one_hop_neighbors(graph: nx.MultiDiGraph, query) -> list | None:
    """ 
    Get one-hop neighbors from networkx graph.

    Args:
        graph (nx.MultiDiGraph): The graph to search in.
        query: The node to find neighbors for.
    Returns:
        list: A list of one-hop neighbors.
        None: If the node is not in the graph.
    """
    try:
        # get one-hop neighbors from networkx graph
        return list(graph.neighbors(query))
    except nx.NetworkXError:
        # if the node is not in the graph, return an empty list
        return None

def two_hop_neighbors(graph: nx.MultiDiGraph, query) -> list:
    # get two-hop neighbors from networkx graph
    one_hop = one_hop_neighbors(graph, query)
    two_hop = []
    for node in one_hop:
        two_hop.extend(one_hop_neighbors(graph, node))
    return list(set(two_hop))

def dfs(graph: nx.MultiDiGraph, query, depth) -> list:
    # perform depth-first search on networkx graph
    visited = []
    stack = [(query, 0)]
    while stack:
        node, level = stack.pop()
        if node not in visited:
            visited.append(node)
            if level < depth:
                stack.extend(
                    [(n, level + 1) for n in one_hop_neighbors(graph, node)]
                )
    return visited

def bfs(graph: nx.MultiDiGraph, query, depth) -> list:
    # perform breadth-first search on networkx graph
    visited = []
    queue = [(query, 0)]
    while queue:
        node, level = queue.pop(0)
        if node not in visited:
            visited.append(node)
            if level < depth:
                queue.extend(
                    [(n, level + 1) for n in one_hop_neighbors(graph, node)]
                )
    return visited


class RepoGraphSearcher:
    """
    Wrapper class to load from config and search for a RepoGraph.
    """
    def __init__(self, config: dict):
        self.config = config
        self.repo_path = config["repository"]["path"]
        self.output_folder = config["output"]["folder"]
        self.graph_path = os.path.join(self.output_folder, "graph.pkl")

        self.graph = load_graph_from_path(self.graph_path)
    
    def one_hop_neighbors(self, query: str) -> list:
        return one_hop_neighbors(self.graph, query)

    def two_hop_neighbors(self, query: str) -> list:
        return two_hop_neighbors(self.graph, query)