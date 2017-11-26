from __future__ import division
import string
import math
import numpy as np

tokenize = lambda doc: doc.lower().split(" ")

document_0 = "China has a strong economy that is growing at a rapid pace. However politically it differs greatly from the US Economy."
document_1 = "At last, China seems serious about confronting an endemic problem: domestic violence and corruption."
document_2 = "Japan's prime minister, Shinzo Abe, is working towards healing the economic turmoil in his own country for his view on the future of his people."
document_3 = "Vladimir Putin is working hard to fix the economy in Russia as the Ruble has tumbled."
document_4 = "What's the future of Abenomics? We asked Shinzo Abe for his views"
document_5 = "Obama has eased sanctions on Cuba while accelerating those against the Russian Economy, even as the Ruble's value falls almost daily."
document_6 = "Vladimir Putin is riding a horse while hunting deer. Vladimir Putin always seems so serious about things - even riding horses. Is he crazy?"
 
all_documents = [document_0, document_1, document_2, document_3, document_4, document_5, document_6]
 
def jaccard_similarity(query, document):
    """Not used for now"""
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)
 
def term_frequency(term, tokenized_document):
    """Tokenized document is the list of tokens(words in a document)"""
    return tokenized_document.count(term)
 
def sublinear_term_frequency(term, tokenized_document):
    count = tokenized_document.count(term)
    if count == 0:
        return 0
    return 1 + math.log(count)
 
def augmented_term_frequency(term, tokenized_document):
    max_count = max([term_frequency(t, tokenized_document) for t in tokenized_document])
    return (0.5 + ((0.5 * term_frequency(term, tokenized_document))/max_count))
 
def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token)))
    return idf_values
 
def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]
    idf = inverse_document_frequencies(tokenized_documents)
    tfidf_documents = []
    for document in tokenized_documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = sublinear_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents

def relevant_terms(tokenized_documents):
    # tokenized_documents = [tokenize(d) for d in documents]
    idf = inverse_document_frequencies(tokenized_documents)
    doc_relevants = []
    for document in tokenized_documents:
        term_relevancies = {}
        for term in document:
            tf = sublinear_term_frequency(term, document)
            term_relevancies[term] = tf*idf[term]
        # find deciles
        vals = np.array([x[1] for x in term_relevancies.items()])
        deciles = np.percentile(vals, np.arange(0, 100, 10))
        # get 7th decile
        decile7 = deciles[6]
        # filter the terms with relevancy vlaues greater than 7th decile
        doc_relevants.append(list(
            filter( lambda x: x[1]>=decile7,
                term_relevancies.items()
            )
        ))
    relevant_terms = set()
    for x in doc_relevants:
        relevant_terms = relevant_terms.union(set([y[0] for y in x]))
    return relevant_terms


if __name__ == '__main__':
    rels = relevant_terms(list(map(tokenize, all_documents)))
    relevant_terms = set()
    for x in rels:
        relevant_terms = relevant_terms.union(set([y[0] for y in x]))
    print(relevant_terms, len(relevant_terms))
