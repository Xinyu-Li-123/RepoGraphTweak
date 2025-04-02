- RepoGraph doesn't include the fully-qualified path to function / classes. For example

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

- Doesn't distinguish between function and methods

- The builtin apis are excluded using a hardcoded list of api names. If someone overwrite the builtin api, won't work

- For class defined within another class, no contain edge will be created

- Two classes with apis of same name would be treated as the same node in the graph

- If two files contains two classes of the same name, I don't know what will happen but I'm sure the two classes can't be correctly separated