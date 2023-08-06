# Attention
- First things to do when clone this monorepo , require python version >= 3.11 and < 4.0
    ```
    $ make init
    ```
- Open vs-code by "Open workspace from file" -> select "backend.code-workspace"
- Before working with any services
    ```
    # go to service source directory

    $ poetry install
    ```


# Create docs guides
- detail instruction to setup mkdocs
    ```
    https://realpython.com/python-project-documentation-with-mkdocs/
    ```
- for monorepo
    ```
    https://github.com/backstage/mkdocs-monorepo-plugin
    ```
- install packages
    ```
    $ poetry add mkdocs "mkdocstrings[python]" mkdocs-material mkdocs-autorefs mkdocs-monorepo-plugin

    run command bellow to init mkdocs for project
    $ poetry run mkdocs new .
    ```
- with vscode install "docstring" extension
- Run docs server
    ```
    $ make mkdocs-serve
    ```
