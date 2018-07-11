#! /bin/bash

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" # /code/deploy/scripts/
ROOT_DIR=$(dirname "$(dirname "$BASE_DIR")") # /code/

DEEPL_SERVER_REPO='https://github.com/the-deep/DEEPL.git'

# Ignore Pull requets
if ! [ "${TRAVIS_PULL_REQUEST}" == "false" ]; then
    echo '[Travis Build] Pull request found ... exiting...'
    exit
fi

if [[ $TRAVIS_BRANCH == "develop" ]] || [[ $TRAVIS_BRANCH == "feature-local-api-resoponse" ]]; then
    # build and push to lite
    echo "PUSHING image for $TRAVIS_BRANCH branch"
    docker build --cache-from thedeep/deepl:latest-lite --tag thedeep/deepl:latest-lite . -f Dockerfile-lite
    docker push thedeep/deepl:latest-lite
fi
