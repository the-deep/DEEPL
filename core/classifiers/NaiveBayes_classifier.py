from core.classifiers.generic_classifier import GenericClassifier

import nltk


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
        self.__classifier = classifier
        self.__labels = labels
        self.__threshold = 0.50 # TODO: auto_calculate this( or maybe let it pass through constructor)

    @classmethod
    def new(cls, feature_selector_obj, labeled_data, **kwargs):
        """
        Creates the classifier model with the labeled data
        @labeled_data: list of tuple -> [(data, label), ... ]
        @kwargs: any extra arguments
        """
        print('GETTING FEATURE SETS for {} elements'.format(len(labeled_data)))
        feature_sets = nltk.classify.apply_features(
                feature_selector_obj.get_features, labeled_data
        )
        # feature_sets = [
            # (feature_selector_obj.get_features(data), label)
            # for (data, label) in labeled_data
        # ]
        print('DONE')
        print('TRAINING CLASSIFIER')
        classifier = nltk.NaiveBayesClassifier.train(feature_sets)
        print('DONE')
        return cls(classifier, feature_selector_obj, classifier.labels())

    def classify(self, input):
        """Function to classify the input."""
        return self.__classifier.classify(
            self.__feature_obj.get_features(input)
        )

    def classify_as_label_probs(self, input):
        """
        Output the labels and their corresponding probabilities(list of tuples)
        """
        features = self.__feature_obj.get_features(input)
        prob_dist = self.__classifier.prob_classify(features)
        return [(label, dist.prob(label)) for label in dist.samples()]

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
        Return the accuracy of the classifier
        """
        test_set = [(self.__feature_obj.get_features(d), l)
                for (d,l) in test_data
        ]
        return nltk.classify.accuracy(self.__classifier, test_set)

def _feature_function(data):
        return {'first': data[0], 'last': data[-1]}

def _test():
    import random
    from nltk.corpus import names
    from core.classifiers.feature_selector import SimpleFeatureSelector
    labeled_names = ( [(name, "male") for name in names.words('male.txt')] + 
            [(name, "female") for name in names.words('female.txt')] )
    random.shuffle(labeled_names)
    train_data, test_data = labeled_names[500:], labeled_names[:500]

    classifier = NaiveBayesClassifier.new(
        SimpleFeatureSelector.new(), train_data
    )
    print(classifier.classify('bibek'))
    print(classifier.get_accuracy(test_data))
    return classifier

if __name__ == '__main__':
    _test()
