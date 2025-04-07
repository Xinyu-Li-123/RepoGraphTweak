import os
import json
import pickle
import toml
import networkx as nx
from repograph.construct_graph import CodeGraph, Tag # Ensure this is the correct import

def load_tags_from_path(tags_path: str) -> list[Tag]:
    """
    Load tags from a JSON file.
    """
    with open(tags_path, 'r') as f:
        tags_raw = json.load(f)
    tags = []
    for tag in tags_raw:
        tags.append(Tag(
            fname=tag["fname"],
            rel_fname=tag["rel_fname"],
            line=tag["line"],
            name=tag["name"],
            kind=tag["kind"],
            category=tag["category"],
            info=tag["info"]
        ))
    return tags

def load_graph_from_path(graph_path: str) -> nx.MultiDiGraph:
    """
    Load a graph from a pickle file.
    """
    with open(graph_path, 'rb') as f:
        graph = pickle.load(f)
    return graph

def convert_tag_to_graph(tags: list[Tag]) -> tuple:
    """
    Convert a tag dictionary to a tuple suitable for adding to the graph.
    """
    graph = CodeGraph.tag_to_graph(None, tags)
    return graph

class RepoGraphConstructor:
    """
    Wrapper class to construct a RepoGraph from a TOML config file.
    """
    def __init__(self, config: dict):
        self.config = config
        self.repo_path = config["repository"]["path"]
        self.output_folder = config["output"]["folder"]
        self.graph_path = os.path.join(self.output_folder, "graph.pkl")
        self.tags_path = os.path.join(self.output_folder, "tags.json")

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.tags = []
        self.G = nx.MultiDiGraph()
    
    @staticmethod
    def load_config(config_path: str):
        """
        Load the configuration file from the given path.
        """
        return toml.load(config_path)

    def construct(self):
        print("🚧 Constructing the code graph...")
        code_graph = CodeGraph(root=self.repo_path)
        chat_fnames_new = code_graph.find_files([self.repo_path])
        self.tags, self.G = code_graph.get_code_graph(chat_fnames_new)

        print("---------------------------------")
        print(f"🏅 Successfully constructed the code graph for repo directory {self.repo_path}")
        print(f"   Number of nodes: {len(self.G.nodes)}")
        print(f"   Number of edges: {len(self.G.edges)}")
        print("---------------------------------")

    def save(self):
        print("💾 Saving graph and tags...")

        with open(self.graph_path, 'wb') as f:
            pickle.dump(self.G, f)
        print(f"🏅 Successfully saved graph to {self.graph_path}")

        with open(self.tags_path, 'w') as f:
            for tag in self.tags:
                line = json.dumps({
                    "fname": tag.fname,
                    "rel_fname": tag.rel_fname,
                    "line": tag.line,
                    "name": tag.name,
                    "kind": tag.kind,
                    "category": tag.category,
                    "info": tag.info,
                })
                f.write(line + "\n")
        print(f"🏅 Successfully saved tags to {self.tags_path}")

if __name__ == "__main__":
    config_path = "config/img_editor.toml"
    config = RepoGraphConstructor.load_config(config_path)

    constructor = RepoGraphConstructor(config)
    constructor.construct()
    constructor.save()
