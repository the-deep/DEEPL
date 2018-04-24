import os

CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://redis:6379')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://redis:6379')
# CELERY_TIMEZONE = TIME_ZONE

# REDIS STORE CONFIG

REDIS_STORE_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_STORE_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_STORE_DB = os.environ.get('REDIS_DB_NUM', '0')
