from repograph.utils import load_config
from repograph.Searcher import RepoGraphSearcher
from pprint import pprint
import argparse

def main():
    parser = argparse.ArgumentParser(description='Search in a code graph of a repository.')
    parser.add_argument('--config', type=str, help='Path to the configuration file.')
    args = parser.parse_args()

    config = load_config(args.config) 
    searcher = RepoGraphSearcher(config)

    user_input_prompt = "Enter a search query (node name) or 'exit' to quit: "
    user_input = input(user_input_prompt)
    while user_input.lower() != "exit":
        # Perform the search
        one_hop = searcher.search_repo(user_input)

        # Print the results
        print(f"One-hop neighbors of {user_input}:")
        pprint(one_hop)

        user_input = input(user_input_prompt)

if __name__ == "__main__":
    main()