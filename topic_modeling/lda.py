from core.helpers.functional import compose, curry2, curried_map, curried_filter
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

from gensim import corpora, models

class LDAModel:
    """
    Latent Dirichilet Allocation Model for Topic Modeling
    """
    def __init__(self):
        """
        Initialize the LDAModel. Initializes with following default functions/values:
        - _tokenizer: RegexpTokenizer(r'\w+').tokenize
        - _stemmer: PorterStemer().stem
        - stop words: english stop words
        """
        # Initialize functions
        self.__tokenizer = RegexpTokenizer(r'\w+').tokenize
        self.__stemmer = PorterStemmer().stem
        # get English stop words
        self.__stop_words = get_stop_words('en')
        # function that returns true if not stop word
        self._not_stop = lambda x: x not in self.__stop_words
        # set the pre_process function
        self.pre_process = self._compose_pre_process_functions()
        self.lda_model = None
        self.dictionary = None

    def _compose_pre_process_functions(self):
        """
        Composes the pre processing functions and return a function
        """
        map_stem = curried_map(self.__stemmer)
        map_lower = curried_map(str.lower) # NOTE: this can also be made pluggable
        return compose(
            list, map_stem, curried_filter(self._not_stop),
            map_lower, self.__tokenizer
        )

    def set_tokenizer(self, tokenizer):
        self.__tokenizer = tokenizer
        self._compose_pre_process_functions()
    def set_stemmer(self, stemmer):
        self.__stemmer = stemmer
        self._compose_pre_process_functions()
    def set_stop_words(self, stop_words):
        self.__stop_words = stop_words
        self._compose_pre_process_functions()

    def create_model(self, documents, num_topics, passes=20):
        """
        Create LDA model.
        @documents - List of documents on which modeling is to be done
        @num_topics - Number of topics to look for
        @passes - Number of passes to run for creating model, higher -> more accurate and slower
        """
        texts = texts = [self.pre_process(document) for document in documents]
        self.dictionary = corpora.Dictionary(texts)
        # CONVERT TO BAG OF WORDS
        corpus = [self.dictionary.doc2bow(text) for text in texts]
        ldamodel = models.ldamodel.LdaModel(
            corpus,
            num_topics=num_topics,
            id2word=self.dictionary,
            passes=passes
        )
        self.lda_model = ldamodel

    def get_topics_and_keywords(self, num_words):
        """Return topics along with the most probable words
        @num_words - Number of most probable/relevant words for each topic
        """
        if not self.lda_model:
            raise Exception("Model not created!! First run create_model(documents, num_topics, passes=20).")

        topics = self.lda_model.get_topics()
        topics_keywords = []
        for topic_words in topics:
            sorted_words = sorted(
                list(enumerate(topic_words)),
                key=lambda x: x[1],
                reverse=True
            )[:num_words]
            topics_keywords.append([(self.dictionary.get(i), x) for i, x in sorted_words])
        return topics_keywords
