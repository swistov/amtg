#! /bin/bash

uvicorn app:app \
  --host $WEB_LISTEN_HOST \
  --port $WEB_LISTEN_PORT \
  --log-level $WEB_LOG_LEVEL
