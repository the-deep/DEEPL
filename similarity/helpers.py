import os

from django.conf import settings

from helpers.utils import get_env_path_or_exception
from classifier.models import ClassifiedDocument


def get_indexed_terms():
    indicespath = get_env_path_or_exception(settings.INDICES_PATH_ENV_VAR)
    filepath = os.path.join(indicespath, settings.TERM_INDEX_FILENAME)
    terms = {}
    with open(filepath, 'r') as f:
        for i, term in enumerate(f.readlines()):
            terms[term.strip()] = i
    return terms


def get_term_frequencies():
    indicespath = get_env_path_or_exception(settings.INDICES_PATH_ENV_VAR)
    filepath = os.path.join(
        indicespath,
        settings.TERM_FREQUENCY_INDEX_FILENAME
    )
    terms_freqs = {}
    with open(filepath, 'r') as f:
        f.readline()  # first line contains num docs, ignore it now
        f.readline()  # next line contains labels
        for data in f.readlines():
            termid, docid, freq = list(map(int, data.split()))
            termdata = terms_freqs.get(termid, {})
            termdata[docid] = freq
            terms_freqs[termid] = termdata
    return terms_freqs


def get_inverse_frequencies():
    indicespath = get_env_path_or_exception(settings.INDICES_PATH_ENV_VAR)
    filepath = os.path.join(
        indicespath,
        settings.INVERSE_FREQUENCY_INDEX_FILENAME
    )
    inv_freqs = {}
    with open(filepath, 'r') as f:
        f.readline()  # first line contains labels
        for data in f.readlines():
            tid, docfreq = list(map(int, data.split()))
            inv_freqs[tid] = docfreq
    return inv_freqs


def get_number_of_documents():
    indicespath = get_env_path_or_exception(settings.INDICES_PATH_ENV_VAR)
    filepath = os.path.join(
        indicespath,
        settings.TERM_FREQUENCY_INDEX_FILENAME
    )
    with open(filepath, 'r') as f:
        data = f.readline()  # It is in the format: #DOCS 100\n
        return int(data.split()[1])


def get_similar_docs(doc, similarity_model, threshold=0.0, limit=None):
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
