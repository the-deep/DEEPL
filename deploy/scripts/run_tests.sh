#!/bin/bash

. /venv/bin/activate

if [ "$CI" == "true" ]; then
    pip install codecov

    coverage run ./manage.py test -v 3
    coverage report
    coverage html
    codecov
else
    pytest -v 3
fi
