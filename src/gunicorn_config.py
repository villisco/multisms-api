from os import environ
# https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py

# ------------------------
# Socket binding
# ------------------------
bind = "0.0.0.0:8080"  # Listen on all interfaces (adjust port if needed)

# ------------------------
# Worker processes
# ------------------------
workers = 2
worker_class = "sync"
worker_connections = 1000 # Max simultaneous clients
timeout = 30        # Seconds before killing a worker
keepalive = 5       # TCP keep-alive (seconds)

# ------------------------
# Logging
# ------------------------
loglevel = environ.get('LOG_LEVEL_GUNICORN', 'INFO')  # debug, info, warning, error, critical
accesslog = "-"    # stdout
errorlog = "-"     # stdout
logger_class = "gunicorn_logger.CustomGunicornLogger"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'