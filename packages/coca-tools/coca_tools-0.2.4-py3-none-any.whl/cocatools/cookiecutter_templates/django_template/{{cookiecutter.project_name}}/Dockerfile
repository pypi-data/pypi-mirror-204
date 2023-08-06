# ATTENTION
# Context dir must be at ./workspace-root

FROM python:3.10.11-slim-buster

#ENV http_proxy http://proxy.hcm.fpt.vn:80
#ENV https_proxy http://proxy.hcm.fpt.vn:80
#ENV no_proxy=localhost,127.0.0.1,::1,172.24.222.112
# ENV LC_ALL=C.UTF-8
# ENV LANG=C.UTF-8

# install debug tool
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    libxml2-dev \
    libxmlsec1-dev \
    gcc \
    python-dev \
    libpq-dev \
    mime-support \
    telnet \
    iputils-ping \
    curl \
    htop \
    vim \
    procps \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# create main directory and logs directory
RUN mkdir -p /app/{src,static} /app/log/{uwsgi,gunicorn,uvicorn}
#    && ls -al /app

WORKDIR /app

# install poetry and dependency
# COPY services/chat_service/poetry.lock services/chat_service/pyproject.toml /app/
COPY ./pyproject.toml /app/
COPY ./src/__init__.py /app/src/
COPY ./README.md /app/

RUN --mount=type=cache,target=/root/.cache/pip,id={{cookiecutter.project_slug}}-image pip3 install --upgrade pip \
    && pip3 install poetry \
    && poetry config virtualenvs.in-project true \
    && poetry install


# copy neccessary files
COPY . /app/


# EXPOSE 5000

CMD ["make", "run-service"]
