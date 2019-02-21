import os
import pickle
import logging

import pandas as pd

from django.conf import settings

from helpers.utils import sparsify_tfidf

logger = logging.getLogger(__name__)


def get_train_test_data(csv_path):
    from classifier.NaiveBayesSKlearn import SKNaiveBayesClassifier
    """csv path points to csv file with sectors and entries"""
    df = pd.read_csv(csv_path)
    processed = df.assign(excerpt=df['excerpt'].apply(
        SKNaiveBayesClassifier.preprocess
    ))
    processed = processed[:100]
    processed = processed.sample(frac=1)
    length = len(processed)
    one_fourth = int(length/4)
    train = processed['excerpt'][one_fourth:]
    test = processed['excerpt'][:one_fourth]
    target = processed['sector'][one_fourth:]
    test_target = processed['sector'][:one_fourth]
    return (train, target), (test, test_target)


def get_dimension_reduced_input(processed_input, meta, classifier_id):
    # Dimension reduction
    dictionary_path = meta.get('dictionary_path')
    tfidf_model_path = meta.get('tfidf_model_path')
    pca_model_path = meta.get('pca_model_path')

    dictionary_full_path = os.path.join(
        settings.CLASSIFIER_DATA_PATH,
        str(classifier_id),
        dictionary_path
    )
    tfidf_full_path = os.path.join(
        settings.CLASSIFIER_DATA_PATH,
        str(classifier_id),
        tfidf_model_path
    )
    pca_full_path = os.path.join(
        settings.CLASSIFIER_DATA_PATH,
        str(classifier_id),
        pca_model_path
    )
    # RELATIVE TO settings.CLASSIFIER_DATA_PATH
    sparsify = meta.get('sparsify', True)
    if dictionary_path is None or pca_model_path is None:
        logger.error('Classification model has dimension_reduction set to true but dictionary_path or pca_model_path missing')  # noqa)
        return None

    dictionary = pickle.load(open(dictionary_full_path, 'rb'))
    tfidf_model = pickle.load(open(tfidf_full_path, 'rb'))
    pca_model = pickle.load(open(pca_full_path, 'rb'))

    bow = dictionary.doc2bow(processed_input.split())

    tfidf_vector = tfidf_model[bow]

    if sparsify:
        tfidf_vector = sparsify_tfidf(tfidf_vector, dictionary)

    # return dim reduced
    return pca_model.transform(tfidf_vector)
