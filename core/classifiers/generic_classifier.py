from core.classifiers.exceptions import ClassifierMethodNotImplemented

class GenericClassifier():
    """
    Base class for all the classifiers.
    This class just provides interfaces for classes that inherit this.
    By default, all methods raise ClassifierMethodNotImplemented exception.
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
        raise ClassifierMethodNotImplemented

    def classify(self, input):
        """Classifies the input as the most relevant/probable label."""
        raise ClassifierMethodNotImplemented

    def multi_label_classify(self, input):
        """Classifies the input as the most relevant/probable labels."""
        raise ClassifierMethodNotImplemented

    def classify_as_label_probs(self, input):
        """
        Classifies the input showing probabilities of all the possible labels.
        """
        raise ClassifierMethodNotImplemented

    def get_accuracy(self):
        """
        Returns the accuracy of the classifier
        """
        raise ClassifierMethodNotImplemented

    def retrain(self, labeled_data):
        """
        Retrain the classifier and return new classifier
        """
        raise ClassifierMethodNotImplemented
