from core.classifiers.exceptions import MethodNotImplemented

class GenericFeatureSelector():
    """
    Generic Feature Selector. Methods available:
    - get_features(input)
    - new()
    """
    def __init__(self):
        pass

    @classmethod
    def new(cls, **kwargs):
        raise MethodNotImplemented

    def get_features(self):
        raise MethodNotImplemented


class SimpleFeatureSelector(GenericFeatureSelector):
    """
    Simple selector, that does not require extra data for feature extraction.
    Used for simple features like gender classification
    """
    def __init__(self):
        pass

    @classmethod
    def new(cls, **kwargs):
        return cls()

    def get_features(self, input):
        """Returns features. input is word"""
        return {
            "first": input[0],
            "last": input[-1]
        }


class DocumentFeatureSelector(GenericFeatureSelector):
    """
    Feature Selector for document classification
    Selects features as word being present in frequent words list or not
    """

    def __init__(self, freq_words):
        self.__freq_words = freq_words

    @classmethod
    def new(cls, **kwargs):
        """
        Returns new object. Takes in frequent words list as freq_words kwarg
        """
        freq_words = []
        if 'freq_words' in kwargs:
            freq_words = kwargs['freq_words']
        return cls(freq_words)

    def get_features(self, input):
        """Returns features of the input text"""
        # First convert input to list of words if necessary
        if type(input) == list:
            inp_words = input
        elif type(input) == str:
            inp_words = str.split(' ')
        else:
            inp_words = []
        inp_dict = {k: True for k in inp_words}
        return {
            'contains({})'.format(x): True if inp_dict.get(x) else False
                for x in self.__freq_words
        }
