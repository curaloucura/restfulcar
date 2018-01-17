#!/usr/bin/env python

import os

bind = '0.0.0.0:%i' % int(os.getenv('PORT', 5000))
backlog = int(os.getenv('GUNICORN_BACKLOG', 2048))


workers = int(os.getenv('WEB_CONCURRENCY', 3))
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'sync')
worker_connections = int(os.getenv('GUNICORN_WORKER_CONNECTIONS', 2000))
max_requests = int(os.getenv('GUNICORN_MAX_REQUESTS', 0))
max_requests_jitter = int(os.getenv('GUNICORN_MAX_REQUESTS_JITTER', 0))
timeout = int(os.getenv('GUNICORN_TIMEOUT', 30))
graceful_timeout = int(os.getenv('GUNICORN_GRACEFUL_TIMEOUT', 0))
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', 2))
threads = int(os.getenv('GUNICORN_THREADS', 1))


reload = bool(os.getenv('GUNICORN_RELOAD', False))
spew = False

daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

errorlog = '-'
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
accesslog = '-'

proc_name = None