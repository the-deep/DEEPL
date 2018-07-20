#!/bin/bash

. /venv/bin/activate
pip3 install -r requirements.txt
rm celerybeat.pid

# Celery Beat
celery -A deepl beat -l info &
# Celery Worker
celery -A deepl worker -l info

