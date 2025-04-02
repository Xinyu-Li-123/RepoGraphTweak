import networkx as nx
import matplotlib.pyplot as plt
import pickle
import sys
import os

# # Create a simple graph
# input_path = sys.argv[1]
# with open(input_path, "rb") as file:
#     G: nx.MultiDiGraph  = pickle.load(file)
# # breakpoint()
# # Draw it

# # remove node with no connection
# G.remove_nodes_from(list(nx.isolates(G)))

# nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=15)

# plt.show()

class RepoGraphVisualizer:
    """
    Wrapper class to visualize a RepoGraph.
    """
    def __init__(self, config: dict):
        self.config = config
        self.output_folder = config["output"]["folder"]
        self.graph_path = os.path.join(self.output_folder, "graph.pkl")
        self.tags_path = os.path.join(self.output_folder, "tags.json")

    def vis_repograph(self):
        """Visualize the whole RepoGraph"""
        print("🚀 Visualizing the repo graph...")
        with open(self.graph_path, "rb") as file:
            G: nx.MultiDiGraph  = pickle.load(file)
        nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=15)
        plt.show()
    
    def vis_egograph(self, term: str, num_hops: int = 1):
        """Visaulzie the ego graph of a term (function / class)"""
        pass 