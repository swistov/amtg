FROM python:3.8-slim

LABEL maintainer="Targyz <targyz@gmail.com>"

ENV PYTHONUNBEFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=off

WORKDIR /app
RUN groupadd -r app && useradd -r -g app app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY --chown=app . .

EXPOSE 19000

USER app
ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "docker/gunicorn_config.py", "app:app"]
