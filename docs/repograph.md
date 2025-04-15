# RepoGraph Specification

## Node

### Unique Identifer of Object

Each node in repograph represents a unique object. The object can be a function, a class, a class method, or a module. To unique identify such an object for any python codebase, even those not designed to be used as a library, we need a robust unique identifier.

We combine relative path and fully-qualified name (FQN) to create a unique identifier for each object of the form `<prefix>::<fqn>`. The spec of the identifier is as follows:

- Function: `<prefix>::<module>.<function>`

- Class: `<prefix>::<module>[.<class>].<class>`

- Class method: `<prefix>::<module>[.<class>].<method>`

- Module: `<prefix>::<module>`

The exact value of `<prefix>` depends on the location of the file that contains the object:

- For item in local file, i.e. file in the repo, `<prefix>` is relative path to the repo root: `./[folder/]<file>.py`. For example, a function `foo()` in `$PROJECT_ROOT/a/b/c.py` will be represented as `./a/b/c.py::c.foo`

- For item in builtin or third-party library, `<prefix>` is `\<external\>`. For example, the class `ArgumentParser` in `argparse` will be represented as `<external>::argparse.ArgumentParser`

Note that, although every Python file is technically a module, not all modules are importable-especially if their parent folders lack `__init__.py`. To ensure consistent identification even for non-importable modules, we don't consider submodules. Instead, we treat the file containing the object as a module, and prefix the FQN with the relative folder path to project root (e.g., For `func` in `$PROJECT_ROOT/a/b/c.py`, we use `./a/b: c.func`), preserving structure even when import resolution fails.

### Unique Identifier of Presence of Object

TODO: There is actually no need to uniquely identify def and ref node in the graph. When we search for an object, we would be interested in

- all its presence in the repo

- any other object that either references or contains it.

As a result, we only need a `networkx.MultiDiGraph` to represent the graph. 

This differs from the description in the paper, but it's more practical, considering that the LM agent only search for a specific object, instead of the specific presence of the object.

<!-- 
Each node in repograph represents not only a unique object, but a unique presence of an object, whether it's definition or reference. Therefore, we need more than just the unique identifier of the object defined above.

To identify the presence of an object, we assign an automatically increasing id to each presence of object reference. This presence id is a number starting from 0, and increasing by 1 for each presence of the object. The exact way we compute this id is irrelavent-all we need is to ensure that the id is unique across all presence of that exact object. We only do so for reference to object, not for the definition of object.

That is,

- For def node, we have node id `<prefix>::<fqn>`

- For ref node, we have node id `<prefix>::<fqn> - <presence_id>`

For example, consider the following three files with the presence of `foo` function:

```python
# ./a/b/file1.py
def foo():
    pass
```

```python
# ./a/b/file2.py
from file1 import foo

def bar():
    foo()
```

```python
# ./a/file3.py
from a.b.file1 import foo

print(foo())
```

In this case, `foo()` is defined in `./a/b/file1.py`, and referenced in `./a/b/file2.py` and `./a/file3.py`. This would results in three nodes with these identifiers:

- `./a/b/file1.py::file1.foo` (definition of `foo`)

- `./a/b/file2.py::file1.foo - 0` (reference of `foo` in `./a/b/file2.py`)

- `./a/file3.py::file1.foo - 1` (reference of `foo` in `./a/file3.py`)
 -->

## Edge