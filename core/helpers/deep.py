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


def get_classifier():
    """ TEMPORARY FUNCTION TO HELP WITH CREATING DEEP DATA"""
    from core.tasks import process_deep_entries_data
    from core.helpers.common import rm_punc_not_nums, rm_stop_words_txt, translate_to_english_txt, compose
    from core.classifiers.feature_selector import DocumentFeatureSelector, BigramFeatureSelector
    from core.classifiers.NaiveBayes_classifier import NaiveBayesClassifier
    import nltk
    from nltk.stem.snowball import SnowballStemmer
    import random
    import langid

    csv_file_path = '_playground/sample_data/nlp_out.csv'

    print('PROCESSING DEEP ENTRIES DATA')
    data = process_deep_entries_data(csv_file_path)[:150]
    print('DONE')

    print('REMOVING PUNC AND STOP WORDS')
    stemmer = SnowballStemmer('english')
    rm_punc_and_stop = compose(
        rm_punc_not_nums,
        rm_stop_words_txt,
        stemmer.stem
    )
    data = [(rm_punc_and_stop(str(ex)), l) for (ex, l) in data if langid.classify(str(ex))[0] == 'en']
    print('DONE')

    print('SHUFFLING DATA')
    random.shuffle(data)
    print('DONE')

    data_len = len(data)
    test_len = int(data_len * 0.4)

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
    # print(freq_words[:200])
    # assert False
    selector = DocumentFeatureSelector.new(corpus=data)#freq_words=freq_words)
    print('DONE')

    # print('CREATING BIGRAM FEATURE SELECTOR')
    # selector = BigramFeatureSelector.new(corpus=data, top=2000)
    # selector = DocumentFeatureSelector.new(corpus=data, top=2000)
    # print('DONE')

    print('CREATING CLASSIFIER')
    classifier = NaiveBayesClassifier.new(selector, rm_punc_and_stop, train_data)
    print('DONE')

    print('ACCURACY', classifier.get_accuracy(test_data))

    print('CONFUSION MATRIX')
    print(classifier.get_confusion_matrix(test_data))
    return classifier
