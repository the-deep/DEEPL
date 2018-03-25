#!/bin/bash -x

# /code/deploy/scripts/
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# /code/
ROOT_DIR=$(dirname $(dirname "$BASE_DIR"))

cd $ROOT_DIR

. /venv/bin/activate
pip3 install -r requirements.txt
export NLP_INDICES_PATH=/code/nlp_indices/
yarn install
webpack
python manage.py migrate --no-input
python manage.py runserver 0.0.0.0:8000
