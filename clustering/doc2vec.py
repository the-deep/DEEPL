import gensim
from nltk import RegexpTokenizer
from nltk.corpus import stopwords

from classifier.models import ClassifiedDocument
from helpers.utils import timeit
from django.conf import settings


tokenizer = RegexpTokenizer(r"\w+")
stopword_set = set(stopwords.words("english"))


def clean_doc(doc):
    lower = doc.lower()
    tokenized = tokenizer.tokenize(lower)
    stopped = [x for x in tokenized if x not in stopword_set]
    return stopped


# ITERATOR for Doc2Vec
class LabeledLineSentence:
    """This will be used as the iterator for doc2vec"""
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield gensim.models.doc2vec.LabeledSentence(
                doc,
                [self.labels_list[idx]]
            )


@timeit
def create_document_vectors():
    docs = ClassifiedDocument.objects.all().values('id', 'text')
    texts = list(map(lambda x: x['text'], docs))
    docids = list(map(lambda x: str(x['id']), docs))
    cleaned_docs = list(map(clean_doc, texts))
    # create iterator
    it = LabeledLineSentence(cleaned_docs, docids)
    model = gensim.models.Doc2Vec(
        size=100, min_count=0, alpha=0.025, min_alpha=0.025
    )
    model.build_vocab(it)

    # training of model
    for epoch in range(100):
        print("iteration {}".format(epoch+1))
        model.train(it, total_examples=model.corpus_count, epochs=model.iter)
        model.alpha -= 0.002
        model.min_alpha = model.alpha
    # saving the created model
    model.save("doc2vec.model")
    print("Document vector for index 1", model.docvecs[1])
    similar_doc = model.docvecs.most_similar(14)
    print(similar_doc)


if __name__ == '__main__':
    create_document_vectors()
