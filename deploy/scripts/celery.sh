#!/bin/bash

. /venv/bin/activate
pip3 install -r requirements.txt

# Celery Beat
celery -A deepl beat -l info &
# Celery Worker
celery -A deepl worker -l info

rm celerybeat.pid
