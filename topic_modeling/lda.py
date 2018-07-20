import numpy as np
from gensim import corpora, models

from helpers.common import preprocess


DOCUMENT_NUM_TOPICS = 2


class LDAModel:
    def __init__(self):
        self.topics_subtopics = None
        self.model = None
        self.dictionary = None

    def get_topics_and_subtopics(
            self, documents, num_topics, num_words,
            depth=3, pre_processing_func=preprocess, passes=10):
        if self.topics_subtopics is not None:
            return self.topics_subtopics
        self.documents = documents
        texts = [
            pre_processing_func(document).split() for document in documents
        ]
        self.dictionary = corpora.Dictionary(texts)
        self.corpus = [self.dictionary.doc2bow(text) for text in texts]
        self.model, self.topics_subtopics = _get_subtopics(
            self.corpus, self.dictionary, num_topics, num_words, depth, passes
        )
        return self.topics_subtopics

    def get_topics_correlation(self, documents, num_topics, num_words):
        # First calculate topics and subtopics
        self.get_topics_and_subtopics(
            documents, num_topics, num_words, depth=1
        )
        topics = self.model.get_document_topics(self.corpus)
        # TODO: get topic names instead of just labels
        document_topics = [x for x in topics]
        '''document_topics is now of the form
            [[(0, 0.028578395456892954),
            (1, 0.028590695375263975),
            (2, 0.88566177734064022),
            (3, 0.02859074725263475),
            (4, 0.028578384574568121)],
            [(0, 0.83994446267426459),
            (1, 0.040021024978900019),
            (2, 0.040005850180507181),
            (3, 0.04002093774612768),
            (4, 0.040007724420200605)]]
        We want vector of each topic'''
        raw_vecs = zip(*document_topics)
        '''Now, raw_vecs is something like this:
        [((0, 0.028578395456892954),
        (0, 0.83994446267426459),
        (0, 0.040007682551798526)),
        ((1, 0.028590695375263975),
        (1, 0.040021024978900019),
        (1, 0.040020920481166559)),
        ((2, 0.88566177734064022),
        (2, 0.040005850180507181),
        (2, 0.040005803525886292))]
        We want to remove first element from each tuple'''
        vectors = [np.asarray([y for x, y in each]) for each in raw_vecs]
        # now normalize
        normalized_vectors = [x/np.linalg.norm(x) for x in vectors]
        # now ready for calculation of correlation
        correlation = {}
        size = len(normalized_vectors)
        for i, x in enumerate(normalized_vectors):
            key = 'Topic {}'.format(i+1)
            correlation[key] = {}
            for j in range(0, size):
                correlation[key]['Topic {}'.format(j+1)] =\
                        np.dot(x, normalized_vectors[j])
        return correlation


def _get_subtopics(
        corpus, dictionary, num_topics, num_words, depth, passes=10
        ):
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
        lda_output['Topic {}'.format(i)] = {
            'keywords': [
                (dictionary.get(i), x)
                for i, x in sorted_words[:num_words]
            ],
            'subtopics': {}
        }
    if depth <= 1:
        return ldamodel, lda_output
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
                # Ignore the model from subsequent call, we are interested in
                # initial model only
                _, lda_output[topic]['subtopics'] = _get_subtopics(
                    topic_docs,
                    dictionary,
                    num_topics,
                    num_words,
                    depth-1
                )
        return ldamodel, lda_output
