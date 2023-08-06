# Require
- Python 3.10 or later but not 4.0
- Working on linux (ubuntu, centos, debian) or unix (macos 13 and higher)

# Initialize
- In Makefile using python3.10, you should use 3.10, if you wanna other version, you could change in pyproject.toml line 10
    ```
    from
        python = "^3.10"
    to
        ptyhon = "your version"
    ```
- If you don't have poetry, just install it then confiugre anythings you need
    ```
    $ pip3.10 install poetry
    ```
- Run command to setup environment
    ```
    $ make poetry-init
    ```


# Docker
- Configure your environment first at ./envs/.env
- Run command to up/restart app container
    ```
    $ make docker-up
    ```
- Other docker command in Makefile, you should prepare database or cache container before up the app container
    Up redis:
    ```
    $ make docker-up-local-redis
    ```
    Up database:
    ```
    $ make docker-up-local-mongo
    ```

# Documents
- Using MkDoc
- To serve
    ```
    $ poetry run mkdocs serve
    ```
