#!/bin/bash

. /venv/bin/activate
pip3 install -r requirements.txt
pkill -9 celery

# Celery Worker
celery -A deepl worker -B -l info
