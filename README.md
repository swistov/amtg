# Description

Experimental service for redirecting AlertManager and sending notification to Telegram Chats

Provives an `/alert` endpoint, that is used for recieving request from AlertManager

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

# Licence

MIT