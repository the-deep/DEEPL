from classifier.exceptions import MethodNotImplemented

from classifier.helpers import get_dimension_reduced_input


class GenericClassifier():
    """
    Base class for all the classifiers.
    Methods provided are:
    - new(labeled_data, **kwargs)
    - classify(input)
    - multi_label_classify(input)
    - classify_as_label_probs(input)
    - get_accuracy()
    - retrain(labeled_data)
    """
    def __init__(self, classifier):
        self.__classifier = classifier

    @classmethod
    def new(cls, labeled_data, **kwargs):
        """Class method to create an instance of classs. """
        raise MethodNotImplemented

    def classify(self, processed_input):
        """Classifies the input as the most relevant/probable label."""
        inp_type = type(processed_input)
        if inp_type == str:
            processed_input = [processed_input]
        prediction = self.__classifier.predict(processed_input)
        return prediction[0] if inp_type == str else prediction

    def multi_label_classify(self, input):
        """Classifies the input as the most relevant/probable labels."""
        raise MethodNotImplemented

    def classify_as_label_probs(
            self, processed_input, meta={}, classifier_id=None):
        """
        Classifies the input showing probabilities of all the possible labels.
        """
        if type(processed_input) == list or type(processed_input) != str:
            raise Exception("The paramerter should be a string, not list")
        if meta:
            inp = get_dimension_reduced_input(
                processed_input, meta, classifier_id)
        else:
            inp = [processed_input]
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
