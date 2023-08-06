PROJECT_DIR:= $(shell pwd)
EXIST_CONTAINER:= $(shell docker ps -aq -f name=afaf3fadsfa-app)

poetry-init:
	poetry env use python3.10
	poetry install


run-local:
	APP_ENV_NAME=local poetry run python run.py

run-dev:
	APP_ENV_NAME=dev poetry run python run.py

run-stg:
	APP_ENV_NAME=stg poetry run python run.py

run-service:
	poetry run python run.py

docker-up-local-redis:
	docker run --name {{cookiecutter.project_slug}}-redis -v ${PROJECT_DIR}/data/redis:/data -p 6379:6379 -d redis redis-server --requirepass password --save 60 1 --loglevel warning


docker-rm-local-redis:
	docker rm -f {{cookiecutter.project_slug}}-redis


docker-up-local-mongo:
	docker run --name {{cookiecutter.project_slug}}-mongo -v ${PROJECT_DIR}/data/mongo:/data/db -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=username -e MONGO_INITDB_ROOT_PASSWORD=password -d mongo


docker-rm-local-mongo:
	docker rm -f {{cookiecutter.project_slug}}-mongo


docker-build:
	docker build -t {{cookiecutter.project_slug}}-app-image .


docker-down:
	if [ -z $(shell docker ps -aq -f name={{cookiecutter.project_slug}}-app) ]; then \
		echo "not found container"; \
	else \
		docker rm -f {{cookiecutter.project_slug}}-app;  \
	fi

docker-up:
	make docker-down
	make docker-build
	docker run --name {{cookiecutter.project_slug}}-app -p {{cookiecutter.port}}:{{cookiecutter.port}} -d {{cookiecutter.project_slug}}-app-image
