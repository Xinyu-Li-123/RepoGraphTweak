from repograph.utils import load_config
from repograph.Visualizer import RepoGraphVisualizer
import argparse

def main():
    parser = argparse.ArgumentParser(description='Visualize a code graph.')
    parser.add_argument('--config', type=str, help='Path to the configuration file.')
    args = parser.parse_args()

    config = load_config(args.config)
    visualizer = RepoGraphVisualizer(config)
    visualizer.vis_repograph()

    # input_term = ""
    # while input_term != "exit":
    #     input_term = input("Enter a term to visualize its ego graph: ")
    #     visualizer.vis_egograph(input_term, num_hops=1)

if __name__ == "__main__":
    main()