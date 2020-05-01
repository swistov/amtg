# Description

Experimental service for recieving, processing events from AlertManager and sending notification to Telegram Chats

Provides an `/alert` endpoint, that is used for recieving events from AlertManager. 

Project status: not even alpha

# Install
```bash
pip install -r requirements
cp .env.exaple .env
```

# Configure

## AMTG
Replace values in `.env` with yours ones.

## Alertmanager config

```yaml
# /etc/alertmanager/alertmanager.yml
# ...
routes:
    - receiver: amtg
      match:
        priority: P1
      continue: true

recievers:
  - name: "amtg"
    webhook_configs:
      - send_resolved: true
        url: http://<host>:<port>/alert

#...

```

# Run

```bash
uvicorn app:app --port 19000
```

Dev mode:

```bash
uvicorn app:app --port 19000 --log-level trace --reload
```

# Docker

## Build

```bash
docker build -t <repo>:<tag>  -f docker/Dockerfile .
```

## Configuration

Environment variables

variable | default | description
---|---|---
BIND_ADDRESS | 0.0.0.0:19000 | gunicorn bind address
LOG_LEVEL | info | gunicorn log level
DEBUG | false |  debug mode
TIMEOUT | 10 sec | gunicorn timeout
DESTINATION_CHAT_ID | none | telegram chat id for notifications 
TELEGRAM_BOT_TOKEN | | Telegram API Token

# Licence

MIT