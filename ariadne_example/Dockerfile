FROM python:3.9-buster

ENV APP_HOME /app

WORKDIR /app

RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install poetry

COPY poetry.lock ${APP_HOME}/poetry.lock
COPY pyproject.toml ${APP_HOME}/pyproject.toml
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY ../.. ${APP_HOME}

CMD ["python", "/app/main.py"]
