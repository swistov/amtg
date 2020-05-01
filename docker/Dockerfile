FROM python:3.8-slim

LABEL maintainer="Targyz <targyz@gmail.com>"

# Common ENV
ENV PYTHONUNBEFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=off

# Uvicorn ENV
ENV WEB_CONCURRENCY=1
ENV WEB_LOG_LEVEL=info
ENV WEB_LISTEN_HOST=0.0.0.0
ENV WEB_LISTEN_PORT=19000

WORKDIR /app

# Non-root user for running application
RUN groupadd -r app && useradd -r -g app app

# Dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY --chown=app . .
RUN chmod +x docker/entrypoint.sh

EXPOSE 19000

USER app

ENTRYPOINT ["/app/docker/entrypoint.sh"]