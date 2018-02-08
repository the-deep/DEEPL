from classifier.models import ClassifiedDocument
from correlation.models import Correlation
from helpers.common import (
    remove_punc_and_nums,
    rm_stop_words_txt
)


def create_correlation_data(version, correlated_entity="subtopics"):
    """
    Creates Correlation object from Classification documents.
    @version: version of the Correlation object
    """
    # first check if the Correlation object with same version exists or not
    try:
        Correlation.objects.get(version=str(version))
        raise Exception("Correlation object of version {} already exists. Provide another version".format(version))
    except Correlation.DoesNotExist:
        pass

    classified_documents = ClassifiedDocument.objects.all()
    classified_documents = [(x.classification_label, x.text) for x in classified_documents]
    correlation = get_documents_correlation(classified_documents)
    correlation_obj = Correlation.objects.create(
        correlated_entity=correlated_entity,
        version=version,
        correlation_data=correlation
    )
    return correlation_obj


def get_documents_correlation(classified_documents):
    """
    @classified_documents : list of tuple (label, text)
    """
    word_count = 0
    word_id = {}  # contains word-> id of the word
    class_words_frequency = {}  # contains classes and the words frequencies
    # iterate through ClassifiedDocument
    for text_class, text in classified_documents:
        # - get text and remove stop words and stem words
        pre_processed_text = remove_punc_and_nums(
            rm_stop_words_txt(text)
        )
        # - get class/label of the text
        if not class_words_frequency.get(text_class):
            class_words_frequency[text_class] = {}

        splitted = pre_processed_text.split()
        # - add the words to words dict if not present
        for x in splitted:
            if x not in word_id:
                word_id[x] = word_count
                word_count += 1
            # - also increment the count of the word for the class
            class_words_frequency[text_class][x] = class_words_frequency[text_class].get(x, 0) + 1

    # transform the dict of words-> count to list of counts where indices are ids of words
    class_words_freq = {
        k: [0]*word_count for k, _ in class_words_frequency.items()
    }
    for k, v in class_words_frequency.items():
        for w, cnt in v.items():
            class_words_freq[k][word_id[w]] = cnt
    # now normalize
    for k, v in class_words_freq.items():
        len_sq = (sum([x**2 for x in v]))**0.5
        class_words_freq[k] = [round(float(x)/len_sq, 6) for x in v]

    # now we have words class matrix
    # calculate dot product for each combination
    correlation = {}
    for x in class_words_freq:
        correlation[x] = {}
        for y in class_words_freq:
            correlation[x][y] = sum([round(a*b, 6) for a,b in zip(class_words_freq[x], class_words_freq[y])])
    return correlation
