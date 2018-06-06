from helpers.common import preprocess

from gensim import corpora, models

DOCUMENT_NUM_TOPICS = 2


def get_topics_and_subtopics(
        documents, num_topics, num_words,
        depth=3, pre_processing_func=preprocess,
        passes=10
        ):
    """
    pre_processing_func should work on tokenized strings
    """
    texts = [pre_processing_func(document) for document in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    return _get_subtopics(corpus, dictionary, num_topics, num_words, depth, passes)


def _get_subtopics(corpus, dictionary, num_topics, num_words, depth, passes=10):
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
