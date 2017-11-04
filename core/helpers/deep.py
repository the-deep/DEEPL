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
    from core.classifiers.feature_selector import DocumentFeatureSelector
    from core.classifiers.NaiveBayes_classifier import NaiveBayesClassifier
    import nltk
    import random
    import langid
    csv_file_path = '_playground/sample_data/nlp_out.csv'
    print('PROCESSING DEEP ENTRIES DATA')
    data = process_deep_entries_data(csv_file_path)
    print('DONE')

    print('REMOVING PUNC AND STOP WORDS')
    rm_punc_and_stop = compose(rm_punc_not_nums, rm_stop_words_txt)
    data = [(rm_punc_and_stop(ex), l) for (ex, l) in data if langid.classify(str(ex))[0] == 'en']
    print('DONE')

    print('GETTING WORDS')
    words = [x for (y,l) in data for x in y.split(' ')]
    print('DONE')

    print('GETTING FREQ DIST')
    all_words = nltk.FreqDist(w.lower() for w in words)
    print('DONE')

    print('SORTING')
    word_freq_list = [(k, v) for k, v in all_words.items()]
    sorted_words = sorted(word_freq_list, key=lambda x: x[1], reverse=True)
    print('DONE')

    print('TAKING MOST FREQ WORDS')
    freq_words = [x[0] for x in sorted_words[:2500]]
    print('DONE')

    print('CREATING FEATURE SELECTOR')
    print(freq_words[:200])
    # assert False
    selector = DocumentFeatureSelector.new(freq_words=freq_words)
    print('DONE')

    print('SHUFFLING DATA')
    random.shuffle(data)
    print('DONE')

    print('TAKING OUT TEST/TRAIN DATA')
    train_data = data[500:]
    print("length of training data", len(train_data))
    test_data = data[:500]
    print('DONE')

    print('CREATING CLASSIFIER')
    classifier = NaiveBayesClassifier.new(selector, train_data)
    print('DONE')

    print('ACCURACY', classifier.get_accuracy(test_data))
    return classifier
