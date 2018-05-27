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
    coverage run -m pytest
    coverage report
    coverage html
    codecov
else
    pytest
fi
