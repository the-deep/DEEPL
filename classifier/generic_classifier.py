from classifier.exceptions import MethodNotImplemented

class GenericClassifier():
    """
    Base class for all the classifiers.
    This class just provides interfaces for classes that inherit this.
    By default, all methods raise MethodNotImplemented exception.
    Methods provided are:
    - new(labeled_data, **kwargs)
    - classify(input)
    - multi_label_classify(input)
    - classify_as_label_probs(input)
    - get_accuracy()
    - retrain(labeled_data)
    """
    def __init__(self):
        pass

    @classmethod
    def new(cls, labeled_data, **kwargs):
        """Class method to create an instance of classs. """
        raise MethodNotImplemented

    def classify(self, input):
        """Classifies the input as the most relevant/probable label."""
        raise MethodNotImplemented

    def multi_label_classify(self, input):
        """Classifies the input as the most relevant/probable labels."""
        raise MethodNotImplemented

    def classify_as_label_probs(self, input):
        """
        Classifies the input showing probabilities of all the possible labels.
        """
        raise MethodNotImplemented

    def get_accuracy(self):
        """
        Returns the accuracy of the classifier
        """
        raise MethodNotImplemented

    def retrain(self, labeled_data):
        """
        Retrain the classifier and return new classifier
        """
        raise MethodNotImplemented

    def calculate_confusion_matrix(self, test_data):
        """
        Confusion matrix for classifier. Set self.__confusion_matrix attribute
        """
        raise MethodNotImplemented

    @property
    def confusion_matrix(self):
        return None
