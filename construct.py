from repograph.utils import load_config
from repograph.Constructor import RepoGraphConstructor
import argparse

def main():
    parser = argparse.ArgumentParser(description='Construct a code graph from a repository.')
    parser.add_argument('--config', type=str, help='Path to the configuration file.')
    args = parser.parse_args()

    config = load_config(args.config) 
    constructor = RepoGraphConstructor(config)
    constructor.construct(use_cache=True)
    constructor.save(use_cache=True)

if __name__ == "__main__":
    main()