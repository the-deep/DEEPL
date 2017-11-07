from core.classifiers.exceptions import MethodNotImplemented
from collections import Counter

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
        self.__freq_words = freq_words[:]

    @classmethod
    def new(cls, **kwargs):
        """
        Returns new object. Takes in frequent words list as freq_words kwarg
        """
        freq_words = []
        top = kwargs.get('top', 0)
        if 'freq_words' in kwargs:
            freq_words = kwargs['freq_words']
        elif 'corpus' in kwargs:
            doc_words = [w for (y, l) in kwargs['corpus'] for w in y.split()]
            words_counter = Counter()
            for x in doc_words:
                words_counter[x]+=1
            sorted_words = sorted(words_counter, key=words_counter.__getitem__, reverse=True)
            if not top: top = int(len(sorted_words)/4)
            freq_words = sorted_words[:top]
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
            'contains({})'.format(x): 1 if inp_dict.get(x) else 0
                for x in self.__freq_words
        }

class BigramFeatureSelector(GenericFeatureSelector):
    """
    This selector is similar to DocumentFeatureSelector but uses bigrams
    """
    def __init__(self, bigrams):
        self.__bigrams = bigrams[:]

    @classmethod
    def new(cls, **kwargs):
        bigrams = []
        top = kwargs.get('top', 0) # extract top frequent bigrams
        if 'bigrams' in kwargs:
            bigrams = kwargs['bigrams']
        elif 'corpus' in kwargs:
            # create bigrams from the corpus
            doc_words = [[w for w in y.split()] for (y, l) in kwargs['corpus']]
            c = Counter() # counter for bigrams
            for words in doc_words:
                for x in zip(words, words[1:]):
                    c[' '.join(x)] +=1
            sorted_bgrams = sorted(c, key=c.__getitem__, reverse=True)
            if not top: top = int(len(sorted_bgrams)/4)
            bigrams = sorted_bgrams[:top]
        return cls(bigrams)

    @staticmethod
    def get_bigrams(input_text):
        splitted = input_text.split()
        return list(zip(splitted, splitted[1:]))

    def get_features(self, input):
        """input is a list"""
        inp_dict = {k: True for k in self.get_bigrams(input)}
        return {
            'contains({})'.format(x): 1 if inp_dict.get(x) else 0
                for x in self.__bigrams
        }
