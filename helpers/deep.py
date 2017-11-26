"""
Helper functions [ DEEP specific ]
"""
def get_all_sectors(df):
    """
    Return raw list of sectors
    @df : DataFrame
    """
    l = []
    for v in df[df['twodim'].notnull()][['twodim']].iterrows():
        for k in v[1].twodim:
            l.append(k['sector'])
    return l

def get_sector_excerpt(df):
    """Return list of tuples with sector and excerpt -> [(excerpt, sector)...]
    @df : DataFrame
    """
    l = []
    for v in df[df['twodim'].notnull()][['twodim','excerpt']].iterrows():
        for k in v[1].twodim:
            l.append((v[1].excerpt, k['sector']))
    return l

def get_sub_sectors_excerpt(df):
    """
    Return list of tuples with sector, subsectors and excerpt
    @df : DataFrame
    """
    l = []
    for v in df[df['twodim'].notnull()][['twodim','excerpt']].iterrows():
        for k in v[1].twodim:
            l.append(([k['sector'], k['subsectors']], v[1].excerpt))
    return l


def get_classifier(num=1000):
    """ TEMPORARY FUNCTION TO HELP WITH CREATING DEEP DATA"""
    from classifier.tasks import process_deep_entries_data
    from helpers.common import (
        rm_punc_not_nums, rm_punc_not_nums_list,
        rm_stop_words_txt, rm_stop_words_txt_list,
        translate_to_english_txt,
        compose
    )
    from classifier.feature_selectors import UnigramFeatureSelector, BigramFeatureSelector
    from classifier.NaiveBayes_classifier import NaiveBayesClassifier
    import nltk
    from nltk.stem.snowball import SnowballStemmer
    from nltk.stem.porter import PorterStemmer
    import random
    from nltk.corpus import names, movie_reviews
    import langid

    csv_file_path = '_playground/sample_data/nlp_out.csv'

    print('PROCESSING DEEP ENTRIES DATA')
    data = process_deep_entries_data(csv_file_path)[:num]
    print('DONE')

    print('REMOVING PUNC AND STOP WORDS')
    stemmer = PorterStemmer()
    rm_punc_and_stop = compose(
        rm_punc_not_nums_list,
        rm_stop_words_txt_list,
        lambda x: list(map(str.lower, x)),
        lambda x: list(map(stemmer.stem,x)) # comment this if we don't need stemming
    )
    rm_punc_and_stop = lambda x: x
    data = [(rm_punc_and_stop(str(ex).split()), l) for (ex, l) in data if langid.classify(str(ex))[0] == 'en']
    print('DONE')

    #data = [(list(movie_reviews.words(fileid)), category)
    #       for category in movie_reviews.categories()
    #      for fileid in movie_reviews.fileids(category)
    #]
    #print(data[0])
    tags_data = {}
    for ex, l in data:
        tags_data[l] = tags_data.get(l, '') + " "+ str(ex)
        
    all_tokenized_documents = list(map(lambda x:x.split(), [v for k, v in tags_data.items()]))

    print('SHUFFLING DATA')
    random.shuffle(data)
    print('DONE')

    data_len = len(data)
    test_len = int(data_len * 0.25)

    print('TAKING OUT TEST/TRAIN DATA')
    train_data = data[test_len:]
    print("length of training data", len(train_data))
    test_data = data[:test_len]
    print('DONE')

    print('COUNTING TAG FREQUENCIES in TRAIN DATA')
    d = {}
    for ex, l in train_data:
        d[l] = d.get(l, 0) + 1
    print(d)
    print('DONE')

    print('CREATING FEATURE SELECTOR')
    from classifier.tf_idf import relevant_terms
    #most_relevant_terms = list(relevant_terms(all_tokenized_documents))
    #selector = UnigramFeatureSelector.new(freq_words=most_relevant_terms)
    selector = UnigramFeatureSelector.new(corpus=data, top=2000) # use top 2000 words
    print('DONE')

    # print('CREATING BIGRAM FEATURE SELECTOR')
    # selector = BigramFeatureSelector.new(corpus=data, top=2000)
    # selector = DocumentFeatureSelector.new(corpus=data, top=2000)
    # print('DONE')

    print('CREATING CLASSIFIER')
    classifier = NaiveBayesClassifier.new(selector, train_data)
    print('DONE')

    print('CALCULATING ACCURACY')
    print(classifier.get_accuracy(test_data))

    print('CONFUSION MATRIX')
    print(classifier.get_confusion_matrix(test_data))

    import pickle
    from classifier.models import ClassifierModel
    c = ClassifierModel(
        name='Naive Bayes',
        version='1.1',
        data=pickle.dumps(classifier)
    )
    return c
