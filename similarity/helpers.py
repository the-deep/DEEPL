import os
import json

from django.conf import settings

from helpers.utils import get_env_path_or_exception
from classifier.models import ClassifiedDocument


def get_indexed_terms():
    indicespath = get_env_path_or_exception(settings.INDICES_PATH_ENV_VAR)
    filepath = os.path.join(indicespath, settings.TERM_INDEX_FILENAME)
    with open(filepath, 'r') as f:
        return json.loads(f.read())


def get_term_frequencies_data():
    """Return dict:
    {"num_docs": <>, "docs_tf": { "<doc id>": {<term id>: <freq>}}}
    """
    indicespath = get_env_path_or_exception(settings.INDICES_PATH_ENV_VAR)
    filepath = os.path.join(
        indicespath,
        settings.TERM_FREQUENCY_INDEX_FILENAME
    )
    with open(filepath, 'r') as f:
        data = json.loads(f.read())
        # indices are str, convert to int
        docs_tf = {}
        for k in data['docs_tf']:
            tmp = {}
            for kk in data['docs_tf'][k]:
                tmp[int(kk)] = data['docs_tf'][k][kk]
            docs_tf[int(k)] = tmp
        data['docs_tf'] = docs_tf
        return data


def get_inverse_frequencies():
    indicespath = get_env_path_or_exception(settings.INDICES_PATH_ENV_VAR)
    filepath = os.path.join(
        indicespath,
        settings.INVERSE_FREQUENCY_INDEX_FILENAME
    )
    with open(filepath, 'r') as f:
        data = json.loads(f.read())
        # convert string indices to int
        temp = {}
        for k in data:
            temp[int(k)] = data[k]
        return temp


# NOTE: not used
def get_number_of_documents():
    indicespath = get_env_path_or_exception(settings.INDICES_PATH_ENV_VAR)
    filepath = os.path.join(
        indicespath,
        settings.TERM_FREQUENCY_INDEX_FILENAME
    )
    with open(filepath, 'r') as f:
        data = f.readline()  # It is in the format: #DOCS 100\n
        return int(data.split()[1])


def get_similar_docs(doc, similarity_model, threshold=0.3, limit=None):
    """
    Return all the docs which are similar to given docs
    @doc: The document(text) which is queried
    @similarity_model: The model which will calculate the similarity
    @threshold: Only the docs with similarity not less than 0.7 are returned
    @limit: If not None, will limit the results to given number
    """
    docs_similarities = []  # [(docid, similarity) ... ]
    docvec = similarity_model.get_text_vector(doc)
    for d in ClassifiedDocument.objects.all().values('id', 'text'):
        vec = similarity_model.get_text_vector(d['text'])
        similarity = similarity_model.cosine_smilarity(docvec, vec)
        if similarity >= threshold:
            docs_similarities.append((d['id'], round(similarity, 5)))
    # sort
    docs_similarities.sort(key=lambda x: x[1])
    if limit:
        docs_similarities = docs_similarities[:limit]
    return docs_similarities
