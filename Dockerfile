FROM ubuntu:16.04

MAINTAINER bewakes bewakepandey@gmail.com

# Update and install common packages with apt
RUN apt-get update -y && \
    apt-get install -y \
        git \
        locales \
        vim \
        curl \
        cron \
        python-dev \
        python3 \
        python3-dev \
        python3-setuptools \
        python3-pip \

        # Required by cloudwatch scripts
        unzip \
        libwww-perl \
        libdatetime-perl

# Support utf-8
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

# Install uwsgi for django
# RUN pip3 install uwsgi

# Install node for react
RUN curl -sL https://deb.nodesource.com/setup_7.x | bash -
RUN apt-get install -y nodejs

# Install yarn for react
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install yarn

WORKDIR /code

RUN pip3 install virtualenv
RUN virtualenv /venv

COPY requirements.txt /code/

RUN . /venv/bin/activate && \
    pip install -r requirements.txt &&  \
    python -c "import nltk; nltk.download('stopwords')" && \
    python -c "import nltk; nltk.download('wordnet')" && \
    python -c "import nltk; nltk.download('punkt')" && \
    python -c "import nltk; nltk.download('averaged_perceptron_tagger')"

COPY . /code/

#CMD ./deploy/scripts/run_prod.sh
