## Local Setup
In docker-compose file, use the the following:
- image: thedeep/deepl:latest-lite
- volumes: nlp_data:/nlp_data
- ports:  '8010:8000'
- depends_on: db
db should be a postgres9.6 image

And in env_file, have the following values:
```
NLP_INDICES_PATH=/code/nlp_data/nlp_indices/
DEEPL_CLSUTERED_DOCS_LABEL_LOCATION=/code/nlp_data/clustered_docs_label.data
DEEPL_CLUSTERING_DATA_LOCATION=/code/nlp_data/clustering/

DOC2VEC_MODELS_LOCATION=/code/nlp_data/doc2vec_data/

DB_NAME=postgres
DB_HOST=db
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432

USE_PAPERTRAIL=False
EBS_HOSTNAME=deepl
EBS_ENV_TYPE=
PAPERTRAIL_HOST=
PAPERTRAIL_PORT=

CLASSPATH=/nlp_resources/stanford-ner-2018-02-27/
STANFORD_MODELS=/nlp_resources/stanford-ner-2018-02-27/classifiers/

CI=true

SENTRY_DSN=
SERVER_ENVIRONMENT=local
```
