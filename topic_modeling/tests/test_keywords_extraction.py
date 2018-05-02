from topic_modeling.keywords_extraction import get_key_ngrams


def test_get_key_ngrams_no_numbers():
    document = """
    Early to bed and early to rise makes a man healthy, wealthy and wise. The
    year 1994 was very special to me because I was born that year.
    """
    # check for all maxgrams, upto 5grams
    for maxgram in range(1, 6):
        data = get_key_ngrams(document, maxgram)
        for x in range(1, maxgram+1):
            key = '{}grams'.format(x)
            assert key in data
            for x in data[key]:
                assert type(x) == tuple  # api test will be list(coz JSON)
                assert len(x) == 2
                assert '1994' not in x[0]  # check not number


def test_get_key_ngrams_with_numbers():
    document = """
    Early to bed and early to rise makes a man healthy, wealthy and wise. The
    year 1994 was very special to me because I was born that year.
    """
    # check for all maxgrams, upto 5grams
    num_present = False
    for maxgram in range(1, 6):
        data = get_key_ngrams(document, maxgram, include_numbers=True)
        for x in range(1, maxgram+1):
            key = '{}grams'.format(x)
            assert key in data
            for x in data[key]:
                assert type(x) == tuple  # api test will be list(coz JSON)
                assert len(x) == 2
                if '1994' in x[0]:
                    num_present = True
    assert num_present, "Number should be present"
