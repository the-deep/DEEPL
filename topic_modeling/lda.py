from helpers.functional import compose, curried_map, curried_filter
from helpers.common import rm_punc_not_nums, lemmatize, get_n_largest
from stop_words import get_stop_words

from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from gensim import corpora, models

DOCUMENT_NUM_TOPICS = 2


class LDAModel:
    """
    Latent Dirichilet Allocation Model for Topic Modeling
    """
    def __init__(self):
        """
        Initialize the LDAModel. Initializes with following default
        functions/values:
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
        # NOTE: this can also be made pluggable
        map_lower = curried_map(str.lower)
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

    def create_model(self, documents, num_topics, passes=10):
        """
        Create LDA model.
        @documents - List of documents on which modeling is to be done
        @num_topics - Number of topics to look for
        @passes - Number of passes to run for creating model
                    higher -> more accurate but slower
        """
        texts = [self.pre_process(document) for document in documents]
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
            topics_keywords.append([
                (self.dictionary.get(i), x) for i, x in sorted_words
            ])
        return topics_keywords

    def get_subtopics_and_keywords(self, levels=3, num_words=5, depth=3):
        """Return topics and subtopics from the texts
        @levels - How deep should the subtopics be
        @num_words - Number of most probable/relevant words for each topic
        """
        """ PSEUDO CODE
        input: [corpus, num_topics, num_words, depth]
        function(*input):
          ldamodel=create_model(corpus, num_topics)
          lda_output = {}
          for topic_words in topics:
            sort_words(topic_words)[:num_words]
            lda_output['TOPIC {}'.format(i)] = {
                'keywords': [sorted_words],
                'subtopics': {}
            }
         if depth == 0:
           return lda_output
        else:
          topic_documents = {} # <topic name> : <documents index set>
          for j, corp in enumerate(corpus):
            topics_prob = ldamodel.get_document_topics(corp).max(threshold or specific num)
            for i, topic in enumerate(topics_prob):
                topic_documents.get('Topic {}'.format(i), set()).add(j)
          # now we have topic wise documents index, populate the lda_output
          for topic in lda_output:
            topic_docs = [corpus[x] for x in topic_documents[topic]]
            lda_output[topic]['subtopics'] = function(topic_docs, num_topics, num_words, depth-1)
          return lda_output
        """
        pass


def get_topics_and_subtopics(
        documents, num_topics, num_words,
        depth=3, pre_processing_func=None,
        passes=40
        ):
    """
    pre_processing_func should work on tokenized strings
    """
    # first lemmatize all the documents
    lemmatizer = WordNetLemmatizer()
    documents = [lemmatize(doc, lemmatizer) for doc in documents]

    if not pre_processing_func:
        # pre processing functions
        tokenizer = RegexpTokenizer(r'\w+').tokenize
        map_rm_punc = curried_map(rm_punc_not_nums)
        stop_words = get_stop_words('en')
        not_stop = lambda x: x not in stop_words and len(x) > 2
        map_lower = curried_map(str.lower)

        # compose the functions into one
        pre_processing_func = compose(
            list,
            curried_filter(not_stop),
            map_rm_punc, map_lower, tokenizer
        )
    texts = [pre_processing_func(document) for document in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    return _get_subtopics(corpus, dictionary, num_topics, num_words, depth, passes)


def _get_subtopics(corpus, dictionary, num_topics, num_words, depth, passes=40):
    """The recursive function"""
    ldamodel = models.ldamodel.LdaModel(
        corpus,
        num_topics=num_topics,
        id2word=dictionary,
        passes=passes
    )
    lda_output = {}
    topics = ldamodel.get_topics()
    for i, topic_words in enumerate(topics):
        sorted_words = sorted(
            list(enumerate(topic_words)),
            key=lambda x: x[1],
            reverse=True
        )
        # words = get_n_largest(
        #    num_words, list(enumerate(topic_words)), lambda x: x[1]
        # )
        lda_output['Topic {}'.format(i)] = {
            'keywords': [
                (dictionary.get(i), x)
                for i, x in sorted_words[:num_words]
                # for i, x in words[:num_words]
            ],
            'subtopics': {}
        }
    if depth <= 1:
        return lda_output
    else:
        topic_documents = {}
        for j, corp in enumerate(corpus):
            topics_prob = sorted(
                ldamodel.get_document_topics(corp),
                key=lambda x: x[1]
            )[:DOCUMENT_NUM_TOPICS]
            for i, topic in enumerate(topics_prob):
                curr_set = topic_documents.get('Topic {}'.format(i), set())
                curr_set.add(j)
                topic_documents['Topic {}'.format(i)] = curr_set
            # Now we have topic wise documents index, populate the lda_output
        for topic in lda_output:
            if topic_documents.get(topic):
                topic_docs = [corpus[x] for x in topic_documents[topic]]
                lda_output[topic]['subtopics'] = _get_subtopics(
                    topic_docs,
                    dictionary,
                    num_topics,
                    num_words,
                    depth-1
                )
        return lda_output
