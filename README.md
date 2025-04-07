This repo attempts to fix several bugs in RepoGraph, and add some extensions to it. The original README file is included in the end of this document for reference.

## Todo List

- [ ] Search for module name, e.g. `argparse`

- [ ] Try using fully-qualified name for function / class

- [ ] Distinguish between function and method

## Bugs

- [ ] Def and Ref nodes are mixed into one node in the graph

- [x] Class methods are not separated, instead they are concatenated into one line with '\n'

- [x] Files under root level is not correctly identified in `CodeGraph.structure` when creating list of tags

- [x] Reference to fields in `Tag` uses string key slicing instead of dot notation, however `Tag` is named tuple instead of dict

- [ ] RepoGraph doesn't include the fully-qualified path to function / classes. For example

    ```python
    def myfunc():
        pass 

    class myclass:
        def __init__(self):
            pass 
        
        def myfunc(self):
            pass
    ```

    There will only be one `myfunc` in the RepoGraph

    As a result, RepoGraph can't work with apis of different classes with duplicate name

- [ ] Doesn't distinguish between function and methods

- [ ] The builtin apis are excluded using a hardcoded list of api names. If someone overwrite the builtin api, won't work

- [ ] For class defined within another class, no contain edge will be created. In general, subclass will not be distinguished from class

    Example: `ImageProcessor` and `ImageLoader`

- [ ] Two classes with apis of same name would be treated as the same node in the graph

    Example `ImageProcessor.open()` and `ImageProcessor.ImageLoader.open()`

- [ ] If two files contains two classes of the same name, I don't know what will happen but I'm sure the two classes can't be correctly separated

## Extensions

- [ ] Search for module name, e.g. `argparse`

- [ ] The search term must be an exact match. I'm not sure if that is good or not. For example, we may be interested in 

  - searching for the context of all methods of a class

  - a fuzzy search for a method name

## Integration

- [ ] Use state command to update repograph after each action

# (Orignal README) RepoGraph: Enhancing AI Software Engineering with Repository-level Code Graph

## 📜 Overview

We introduce RepoGraph, an effective plug-in repo-level module that offers the desired context and substantially boosts the LLMs' AI software engineering capability.

## 🆕 News

We released the first version RepoGraph and its integration with [SWE-bench](https://www.swebench.com/) methods!

## 🤖 Code Setup

### Foder and files

`repograph` contains the code for construct and retrieve related context from the graph. 

`agentless` and `SWE-agent` incorporates the integrated version of RepoGraph with the two methods.

Currently this version may take a little long time to run for a repo. We provide a cached version for all repos in SWE-bench, download it from [huggingface datasets](https://huggingface.co/datasets/MrZilinXiao/RepoGraph) or [Google Drive](https://drive.google.com/file/d/1-0d-OgGoOf3i54bWcf8H0egjQyTSZ8dG/view?usp=sharing) and put it under `repo_structures`.

### How to run?

To generate the repograph for a given repository, simply run:

```bash
python ./repograph/construct_graph.py <dir_to_repo>
```

This will produce two files, `tags_{instance_id}.jsonl` stores the line-level information and `{instance_id}.pkl` is the graph constructed using networkx.

## Integration with models on SWE-bench

### Procedural framework

For a procedural framework, RepoGraph could be integrated into every step of the pipeline. Refer to `--repo_graph` hyperparameter for controllability in different stages.

To run RepoGraph with Agentless, use command:

```bash
bash run_repograph_agentless.sh
```

### Agent framework

To integrate RepoGraph with agent framework such as SWE-agent, we simply add an extra action in its initial action space. Specifically, you can look up for `search_repo()` in corresponding dir. The signature is defined as:

```python
search_repo:
    docstring: searches in the current repository with a specific function or class, and returns the def and ref relations for the search term.
    signature: search_repo <search_term>
    arguments:
      - search_term (string) [required]: function or class to look for in the repository.
```

To run RepoGraph with SWE-agent, use command:

```bash
bash run_repograph_sweagent.sh
```

We are working on prepreints for details in RepoGraph and a more comprehensive/easy integration with exsiting models. Stay tuned!!
