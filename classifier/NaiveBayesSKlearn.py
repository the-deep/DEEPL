from classifier.generic_classifier import GenericClassifier

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

import numpy as np

from helpers.functional import curried_map, curried_filter, curried_zip
from helpers.common import (
    rm_punc_not_nums, rm_punc_not_nums_list,
    rm_stop_words_txt, rm_stop_words_txt_list,
    remove_punc_and_nums,
    translate_to_english_txt,
    compose
)

import logging
logger = logging.getLogger(__name__)


class SKNaiveBayesClassifier(GenericClassifier):
    """
    Wrapper around scikit learn Naive Bayes classifier
    """
    def __init__(self, classifier_pipeline):
        self.__classifier = classifier_pipeline

    @staticmethod
    def preprocess(inp):
        func = compose(
            rm_punc_not_nums,
            rm_stop_words_txt,
            ' '.join,
            str.split,
            str.lower,
            str
        )
        return func(inp)

    @classmethod
    def new(cls, train_labeled=None, train=None, target=None):
        """
        Create a new classifier
        """
        text_clf = Pipeline([
            ('vect', CountVectorizer(ngram_range=(1,2))),
            ('tfidf', TfidfTransformer(use_idf=False)),
            ('clf', MultinomialNB(alpha=0.01, fit_prior=False))
        ])
        if train is None or target is None:
            train, target = zip(*train_labeled)
        txt_clf = text_clf.fit(train, target)
        return cls(txt_clf)

    def classify(self, processed_input):
        inp_type = type(processed_input)
        if inp_type == str:
            processed_input = [processed_input]
        prediction = self.__classifier.predict(processed_input)
        return prediction[0] if inp_type == str else prediction

    def classify_as_label_probs(self, processed_input):
        inp_type = type(processed_input)
        classes = self.__classifier.classes_
        prediction = self.__classifier.predict_proba(processed_input)
        prediction = list(
            map(lambda pred: sorted(zip(classes, pred), key=lambda x:x[1], reverse=True),
                prediction
            )
        )
        return prediction[0]

    def get_accuracy(self, test_labeled=None, test=None, target=None):
        if test is None or target is None:
            test, target = zip(*test_labeled)
        predicted = self.__classifier.predict(test)
        return np.mean(predicted == target)

    def get_confusion_matrix(self, test_labeled):
        pass
