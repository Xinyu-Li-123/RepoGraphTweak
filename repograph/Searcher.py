import networkx as nx
import os

from repograph.Constructor import load_graph_from_path, load_tags_from_path

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

class SearchType:
    """
    Enum class for search types.
    """
    ONE_HOP = "ONE_HOP"
    TWO_HOP = "TWO_HOP"
    # DFS and BFS are currently not supported
    DFS = "DFS"
    BFS = "BFS"

    @staticmethod
    def from_string(type_str: str):
        """
        Convert a string to a SearchType.
        """
        if type_str == "ONE_HOP":
            return SearchType.ONE_HOP
        elif type_str == "TWO_HOP":
            return SearchType.TWO_HOP
        else:
            raise ValueError(f"Unsupported search type: {type_str}")

class RepoGraphSearcher:
    """
    Wrapper class to load from config and search for a RepoGraph.
    """
    def __init__(self, config: dict):
        self.config = config
        self.repo_path = config["repository"]["path"]
        self.output_folder = config["output"]["folder"]
        self.graph_path = os.path.join(self.output_folder, "graph.pkl")
        self.tags_path = os.path.join(self.output_folder, "tags.json")
        self.graph = load_graph_from_path(self.graph_path)
        self.tags = load_tags_from_path(self.tags_path)
        self.name2tag = {
            tag["name"]: tag for tag in self.tags
        }
        if "search" not in self.config or "type" not in self.config["search"]:
            # default to one-hop search
            self.search_type = SearchType.ONE_HOP
        else:
            self.search_type = SearchType.from_string(
                self.config["search"]["type"]
            )

    def search_repo(self, query: str) -> list[dict]:
        """
        Searches the repograph for the usage of a specific function, class, or module by exact name,
        and returns detailed information about neighboring nodes in the graph.

        RepoGraph is a directed graph where each node represents lines of code that either define or reference a function, 
        class, or module, and an edge represent two types of relationships between nodes
        - reference: Occur between same category of node (e.g. both are functions). 
            If node A defines a function and node B calls that function, there will be a directed edge from A to B.
        - contain: Occur from class node to function node. If node A defines a class 
            and node B defines a method of that class, there will be a directed edge from A to B.

        Arguments:
            query (str): The exact name of the function, class, or module to search for.
                Must match exactly, partially-matched names, variable names, or file names are not supported.

        Returns:
            list[dict]: A list of entries (functions / classes / modules) connected to the query node (of type def), where each entry contains:
                - name (str): The name of the entry.
                - kind (str): The kind of the node ("def" or "ref").
                - category (str): The category of the entry (e.g., function, class).
                - file (str): The relative path of the file containing the entry.
                - line (list[int]): The start and end line numbers of the entry in the file.
                - info (str): 
                    - For functions or modules: the lines of code using or defining them.
                    - For classes: a '\n'-separated list of its method names.
        
        Example:
            Reference relationship:
                For the following code:
                ```python
                # mymodule/example.py
                1 def foo(num):
                2    print(num)
                
                3 foo(42)
                ```
                `search_repo("foo")` will return:
                ```json
                [
                    {
                        "fname": "mymodule/example.py",
                        "line": [1, 2],
                        "name": "foo",
                        "kind": "def",
                        "category": "function",
                        "info": "def foo(num):\n   print(num)"
                    },
                    {
                        "fname": "mymodule/example.py",
                        "line": [3],
                        "name": "foo",
                        "kind": "ref",
                        "category": "",
                        "info": "foo(42)"
                    }
                ]
                ```
            
            Contain relationship:
                For the following code:
                ```python
                # mymodule/example.py
                1 class Foo:
                2     def bar(self, num):
                3         print(num)
                4
                5     def baz(self):
                6         print("baz")
                ```
                `search_repo("bar")` will return:
                ```json
                [
                    {
                        "fname": "mymodule/example.py",
                        "line": [1, 3],
                        "name": "Foo",
                        "kind": "def",
                        "category": "class",
                        "info": "
                    },
                    {
                        "fname": "mymodule/example.py",
                        "line": [2, 3],
                        "name": "bar",
                        "kind": "def",
                        "category": "function",
                        "info": "bar\nbaz"
                    }
                ]
                ```
        """
        # Note that there won't be any duplicates in the result
        neighbor_ids = self._search_neighbor_on_graph(query)

        # obtain detailed information of the neighbors
        neighbors = []
        for neighbor_id in neighbor_ids:
            neighbors.append(self._id2detail(neighbor_id))
        return neighbors

    def _search_neighbor_on_graph(self, query: str) -> list[str]:
        """
        Search for neighbors of a node in the graph. Return a list of neighbor node ids.
        """
        neighbor_ids = []
        if self.search_type == SearchType.ONE_HOP:
            neighbor_ids = one_hop_neighbors(self.graph, query)
        elif self.search_type == SearchType.TWO_HOP:
            neighbor_ids = two_hop_neighbors(self.graph, query)
        else:
            raise ValueError(f"Unsupported search type: {self.search_type}")
        return neighbor_ids

    def _id2detail(self, node_id: str) -> dict:
        """
        Get the details of a node in the graph.

        Args:
            node_id (str): The node id to get details for.
        
        Returns:
            dict: A dictionary containing the details of the node. The keys are
            - fname (str): The relative path to the file that contains the node.
            - line (list[int]): The start and end line numbers of the node.
            - name (str): The name of the node.
            - kind (str): The type of the node (def or ref)
            - category (str): The category of the node (function, class, etc.)
            - info (str): The additional information of the node. 
                For functions / modules, this is the lines of code; 
                for classes, this is the class methods concatenated with '\n'
        """
        if node_id in self.name2tag:
            tag = self.name2tag[node_id]
            return {
                "fname": tag["fname"],
                "line": tag["line"],
                "name": tag["name"],
                "kind": tag["kind"],
                "category": tag["category"],
                "info": tag["info"]
            }
        else:
            return {
                "fname": "",
                "line": [],
                "name": node_id,
                "kind": "",
                "category": "",
                "info": ""
            }

    def _one_hop_neighbors(self, query: str) -> list:
        return one_hop_neighbors(self.graph, query)

    def _two_hop_neighbors(self, query: str) -> list:
        return two_hop_neighbors(self.graph, query)