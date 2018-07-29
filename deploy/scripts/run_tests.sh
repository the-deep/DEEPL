#!/bin/bash -e

. /venv/bin/activate

if [ "$CI" == "true" ]; then
    . /venv/bin/activate
    pip install -r requirements.txt
    python -c "import nltk; nltk.download('stopwords')"
    python -c "import nltk; nltk.download('wordnet')"
    python -c "import nltk; nltk.download('punkt')"
    python -c "import nltk; nltk.download('averaged_perceptron_tagger')"
    pip install codecov
    NO_CAMELCASE_MIDDLEWARE=true coverage run -m pytest  # because all test cases have snakecase
    coverage report
    coverage html
    codecov
else
    NO_CAMELCASE_MIDDLEWARE=true pytest
fi
