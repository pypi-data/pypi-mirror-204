PROJECT_DIR:= $(shell pwd)
EXIST_CONTAINER:= $(shell docker ps -aq -f name=afaf3fadsfa-app)
POETRY_RUN=poetry run
PYTHON=poetry run python



poetry-init:
	poetry env use python3.10
	poetry install

migrate:
	${PYTHON} manage.py migrate
makemigrations:
	${PYTHON} manage.py makemigrations
collectstatic:
	${PYTHON} manage.py collectstatic --noinput
createsuperuser:
	${PYTHON} manage.py createsuperuser


run-local:
	APP_ENV_NAME=local poetry run python manage.py runserver

run-dev:
	APP_ENV_NAME=dev poetry run python run.py

run-stg:
	APP_ENV_NAME=stg poetry run python run.py

run-service:
	make makemigrations
	make migrate
	make collectstatic
	# poetry run gunicorn -c ${PROJECT_DIR}/configs/gunicorn_config.py src.project.wsgi
	poetry run python manage.py runserver {{cookiecutter.host}}:{{cookiecutter.port}}


docker-up-local-redis:
	docker run --name {{cookiecutter.project_slug}}-redis -v ${PROJECT_DIR}/data/redis:/data -p 6379:6379 -d redis redis-server --requirepass password --save 60 1 --loglevel warning


docker-rm-local-redis:
	docker rm -f {{cookiecutter.project_slug}}-redis


docker-up-local-postgres:
	docker run --name {{cookiecutter.project_slug}}-postgres -v ${PROJECT_DIR}/data/postgres:/var/lib/postgresql/data -p 5432:5432 -e PGDATA=/var/lib/postgresql/data/pgdata -e  POSTGRES_USER=username -e POSTGRES_PASSWORD=password -e POSTGRES_DB=dev -d postgres


docker-rm-local-postgres:
	docker rm -f {{cookiecutter.project_slug}}-postgres


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
