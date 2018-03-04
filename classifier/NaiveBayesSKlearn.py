from classifier.generic_classifier import GenericClassifier

from sklearn.feature_extraction.text import CountVectorizer
from nltk.metrics import ConfusionMatrix
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

import numpy as np

from helpers.common import (
    # rm_punc_not_nums,
    remove_punc_and_nums,
    rm_stop_words_txt,
    compose,
    lemmatize
)

import logging
logger = logging.getLogger(__name__)


class SKNaiveBayesClassifier(GenericClassifier):
    """
    Wrapper around scikit learn Naive Bayes classifier
    """
    def __init__(self, classifier_pipeline):
        self.__classifier = classifier_pipeline
        self.__confusion_matrix = None

    @staticmethod
    def preprocess(inp):
        func = compose(
            ' '.join,
            str.split,
            str.lower,
            remove_punc_and_nums,
            lemmatize,
            rm_stop_words_txt,
            str
        )
        return func(inp)

    @classmethod
    def new(cls, train_labeled=None, train=None, target=None):
        """
        Create a new classifier
        """
        text_clf = Pipeline([
            ('vect', CountVectorizer(ngram_range=(1, 2))),
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
        inp = processed_input.split()
        classes = self.__classifier.classes_
        prediction = self.__classifier.predict_proba(inp)
        prediction = list(
            map(
                lambda pred: sorted(
                    zip(classes, pred),
                    key=lambda x: x[1],
                    reverse=True
                ),
                prediction
            )
        )
        return prediction[0]

    def get_accuracy(self, test_labeled=None, test=None, target=None):
        if test is None or target is None:
            test, target = zip(*test_labeled)
        predicted = self.__classifier.predict(test)
        return np.mean(predicted == target)

    def calculate_confusion_matrix(self, test_data):
        """
        calculate confusion_matrix
        """
        correct_tags = [l for txt, l in test_data]
        predicted_tags = [self.classify(txt) for txt, l in test_data]
        cm = ConfusionMatrix(correct_tags, predicted_tags)
        logger.info(cm)
        self.__confusion_matrix = cm
        return cm

    @property
    def confusion_matrix(self):
        return self.__confusion_matrix

    def retrain(self, labeled_data):
        clf = self.__classifier  # actually this is pipeline
        x, Y = zip(*labeled_data)
        steps = list(clf.named_steps.keys())
        for step in steps[:-1]:
            x = clf.named_steps[step].transform(x)

        clf.named_steps[steps[-1]].partial_fit(
            x, Y, classes=clf.classes_
        )
        return self
