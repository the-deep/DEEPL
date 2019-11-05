#!/bin/bash -x

# /code/deploy/scripts/
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# /code/
ROOT_DIR=$(dirname $(dirname "$BASE_DIR"))

cd $ROOT_DIR

. /venv/bin/activate
pip3 install -r requirements.txt
export NLP_INDICES_PATH=/code/nlp_indices/
if [[ $INSTANCE_TYPE != 'CELERY' ]]; then
    yarn install
    yarn global add webpack-cli@3.1.2 webpack@4.23.1
    webpack
    python manage.py collectstatic
    python manage.py migrate --no-input
    uwsgi --ini $ROOT_DIR/deploy/uwsgi.ini --static-map /static=/static  # Start uwsgi server
    # python manage.py runserver 0.0.0.0:8000
else
    celery -A deepl worker -B -l info
fi

