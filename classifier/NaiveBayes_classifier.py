from classifier.generic_classifier import GenericClassifier

import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.metrics import ConfusionMatrix
from collections import Counter

from helpers.common import (
    rm_punc_not_nums,
    rm_stop_words_txt,
    compose,
    lemmatize
)

import logging
logger = logging.getLogger(__name__)


def identity(x):
    return x


class NaiveBayesClassifier(GenericClassifier):
    """
    This class just wraps the nltk NaiveBayesClassifier and implements
    methods provided by GenericClassifier.
    NOTE: Call the "new" @classmethod instead of directly creating instance.
    """
    def __init__(self, classifier, feature_selector_obj, labels):
        """
        Takes in actual classifier instance, feature function and all labels
        """
        self.__feature_obj = feature_selector_obj
        self.__pre_processor = identity
        self.__classifier = classifier
        self.__labels = labels
        self.__threshold = 0.50
        self.__confusion_matrix = None
        # TODO: auto_calculate threshold(or maybe pass through constructor)
        self.__stemmer = SnowballStemmer('english')

    @staticmethod
    def preprocess(inp):
        inp = lemmatize(inp)
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
    def new(cls, feature_selector_obj, labeled_data, **kwargs):
        """
        Creates the classifier model with the labeled data
        @labeled_data: list of tuple -> [(data, label), ... ]
        @kwargs: any extra arguments
        """
        logger.info('GETTING FEATURE SETS for {} elements'.format(len(labeled_data)))
        feature_sets = nltk.classify.apply_features(
                feature_selector_obj.get_features, labeled_data
        )
        # feature_sets = [
            # (feature_selector_obj.get_features(data), label)
            # for (data, label) in labeled_data
        # ]
        logger.info('DONE')
        logger.info('TRAINING CLASSIFIER')
        classifier = nltk.NaiveBayesClassifier.train(feature_sets)
        logger.info('DONE')
        return cls(classifier, feature_selector_obj, classifier.labels())

    def set_pre_processor(self, func):
        """Set the pre processor function, if not set, it is identity function"""
        self.__pre_processor = func

    def classify(self, input):
        """Function to classify the input."""
        return self.__classifier.classify(
            self.__feature_obj.get_features(self.__pre_processor(input))
        )

    def classify_as_label_probs(self, input):
        """
        Output the labels and their corresponding probabilities(list of tuples)
        """
        features = self.__feature_obj.get_features(self.__pre_processor(input))
        prob_dist = self.__classifier.prob_classify(features)
        return [(label, prob_dist.prob(label)) for label in prob_dist.samples()]

    def multi_label_classify(self, input):
        """
        Output multiple relevant/probable labels for the input. This uses output
        from self.classify_as_label_probs and returns labels whose probability
        exceed some threshold.
        """
        labels_probs = self.classify_as_label_probs(input)
        return list(
            filter(lambda l, p: p >= self.__threshold,
                labels_probs)
        )

    def get_accuracy(self, test_data):
        """
        Return the accuracy of the classifier.
        """
        test_set = [(self.__feature_obj.get_features(d), l)
                for (d,l) in test_data
        ]
        return nltk.classify.accuracy(self.__classifier, test_set)

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

    def calculate_fscore(self, test_data):
        """
        Calculate precision, recall and fscore for each class.
        Return dict containing precision, recall, fscore for each class
        """
        cm = self.get_confusion_matrix(test_data)
        labels = self.__labels
        true_positives = Counter()
        false_negatives = Counter()
        false_positives = Counter()
        for i in labels:
            for j in labels:
                if i == j:
                    true_positives[i] += cm[i,j]
                else:
                    false_negatives[i] += cm[i,j]
                    false_positives[j] += cm[i,j]
        scores = {}
        for i in sorted(labels):
            if true_positives[i] == 0:
                fscore = 0
                scores[i] = {'precision':0, 'recall': 0, 'fscore':0}
            else:
                precision = true_positives[i] / float(true_positives[i]+false_positives[i])
                recall = true_positives[i] / float(true_positives[i]+false_negatives[i])
                fscore = 2 * (precision * recall) / float(precision + recall)
                scores[i] = {'precision':precision, 'recall': recall, 'fscore':fscore}
        return scores



def _feature_function(data):
        return {'first': data[0], 'last': data[-1]}

def _test():
    import random
    from nltk.corpus import names, movie_reviews
    from core.feature_selectors import (
        SimpleFeatureSelector,
        UnigramFeatureSelector
    )
    # labeled_names = ( [(name, "male") for name in names.words('male.txt')] + 
            # [(name, "female") for name in names.words('female.txt')] )
    # random.shuffle(labeled_names)
    # train_data, test_data = labeled_names[500:], labeled_names[:500]


    movie_documents = [(list(movie_reviews.words(fileid)), category)
        for category in movie_reviews.categories()
        for fileid in movie_reviews.fileids(category)
    ]
    random.shuffle(movie_documents)

    all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
    word_features = list(all_words)[:2000]
    print(word_features[:250])

    movie_classifier = NaiveBayesClassifier.new(
            UnigramFeatureSelector.new(freq_words=word_features), lambda x: x,movie_documents[500:]
    )
    print(movie_classifier.get_accuracy(movie_documents[:500]))
    print(movie_classifier.get_confusion_matrix(movie_documents[:500]))
    return movie_classifier

    classifier = NaiveBayesClassifier.new(
        SimpleFeatureSelector.new(), train_data
    )
    print(classifier.classify('bibek'))
    print(classifier.get_accuracy(test_data))
    return classifier

if __name__ == '__main__':
    _test()
