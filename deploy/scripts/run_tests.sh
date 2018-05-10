#!/bin/bash

. /venv/bin/activate

if [ "$CI" == "true" ]; then
    pip install codecov
    coverage run -m pytest
    coverage report
    coverage html
    codecov
else
    pytest
fi
