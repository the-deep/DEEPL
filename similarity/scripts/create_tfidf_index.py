import os
import json

from django.conf import settings

from helpers.utils import merge_lists, get_env_path_or_exception
from classifier.models import ClassifiedDocument
# SKNaiveBayesClassifier is only for preprocessing function
from classifier.NaiveBayesSKlearn import SKNaiveBayesClassifier


def create_terms_index(terms):
    """
    Create terms index in file
    @terms: list of terms ["a", "apple", ...]
    """
    print('Creating term index ...')
    path = get_env_path_or_exception(settings.INDICES_PATH_ENV_VAR)
    terms.sort()
    with open(os.path.join(path, settings.TERM_INDEX_FILENAME), 'w') as f:
        for term in terms:
            f.write(term + "\n")
    print('Successfully created term index')


def create_tf_index(docs):
    """
    Create index, store inverted inedices
    @docs: [{'text': <document text>, 'id': <document id>} ... ]
    """
    all_terms = {}
    all_sorted_terms = []
    idf_counts = {}
    for doc in docs:
        processed = SKNaiveBayesClassifier.preprocess(doc['text'])
        # remove 'nn' which mean numbers
        processed = processed.replace('nn', '')
        terms_freq = {}
        for term in processed.split():
            terms_freq[term] = terms_freq.get(term, 0) + 1
            all_terms[term] = True

        # update idf values
        for t in terms_freq:
            idf_counts[t] = idf_counts.get(t, 0) + 1

        # sort terms_freq, convert to tuple and append doc id
        sorted_terms = list(map(
            lambda x: (*x, doc['id']),
            sorted(terms_freq.items(), key=lambda x: x[0])
        ))
        all_sorted_terms = merge_lists(
            all_sorted_terms,
            sorted_terms,
            key=lambda x: x[0]
        )
    terms = list(all_terms.keys())
    terms_ids = {x: i for i, x in enumerate(sorted(terms))}
    # create terms_index
    create_terms_index(terms)
    # now create tf index
    path = get_env_path_or_exception(settings.INDICES_PATH_ENV_VAR)
    filepath = os.path.join(path, settings.TERM_FREQUENCY_INDEX_FILENAME)
    # write to file
    with open(filepath, 'w') as f:
        f.write('#DOC {}\n'.format(len(docs)))  # Write len(docs) to first line
        f.write('TERMID DOCID TERM_FREQ\n')
        for t, fr, d in all_sorted_terms:
            f.write('{} {} {}\n'.format(
                terms_ids[t], d, fr
            ))
    # also create idf index
    filepath = os.path.join(path, settings.INVERSE_FREQUENCY_INDEX_FILENAME)
    with open(filepath, 'w') as f:
        f.write('TERMID #DOCS\n')
        for t in terms:
            f.write('{} {}\n'.format(terms_ids[t], idf_counts[t]))
    print('Writing indices... DONE')


def create_compressed_tf_index_file(docs):
    """
    Create index, store inverted inedices
    @docs: [{'text': <document text>, 'id': <document id>} ... ]
    """
    all_terms = {}
    docs_terms_freq = {}
    idf_counts = {}
    terms_count = 0
    docslen = len(docs)
    for doc in docs:
        processed = SKNaiveBayesClassifier.preprocess(doc['text'])
        # remove 'nn' which mean numbers
        processed = processed.replace('nn', '')
        terms_freq = {}
        for term in processed.split():
            if not all_terms.get(term):
                all_terms[term] = terms_count
                terms_count += 1
            terms_freq[all_terms[term]] = terms_freq.get(term, 0) + 1

        # update idf values
        for t in terms_freq:
            idf_counts[t] = idf_counts.get(t, 0) + 1

        docs_terms_freq[doc['id']] = terms_freq

    path = get_env_path_or_exception(settings.INDICES_PATH_ENV_VAR)

    # create terms index
    termspath = os.path.join(path, settings.TERM_INDEX_FILENAME)
    with open(termspath, 'w') as f:
        f.write(json.dumps(all_terms))

    filepath = os.path.join(path, settings.TERM_FREQUENCY_INDEX_FILENAME)
    data = {'num_docs': docslen, 'docs_tf': docs_terms_freq}
    # create tf index
    with open(filepath, 'w') as f:
        f.write(json.dumps(data))
    # create idf index
    idfpath = os.path.join(path, settings.INVERSE_FREQUENCY_INDEX_FILENAME)
    with open(idfpath, 'w') as f:
        f.write(json.dumps(idf_counts))


def create_tf_index_for_classified_docs():
    docs = ClassifiedDocument.objects.all().values('id', 'text')
    # create_tf_index(docs)
    create_compressed_tf_index_file(docs)


def main(*args):
    create_tf_index_for_classified_docs()
