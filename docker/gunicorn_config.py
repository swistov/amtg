import os
loglevel = os.getenv("LOG_LEVEL", "info")
workers = 2
bind = os.getenv("BIND_ADDRESS", "0.0.0.0:19000")
errorlog = '-'
accesslog = '-'
timeout = int(os.getenv("TIMEOUT", "10"))
