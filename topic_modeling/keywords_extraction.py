from rake_nltk import Rake

def get_key_unigrams_bigrams(document):
    r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.
    # r = Rake(<language>) # To use it in a specific language supported by nltk.
    # If you want to provide your own set of stop words and punctuations to
    # r = Rake(<list of stopwords>, <string of puntuations to ignore>)
    r.extract_keywords_from_text(document.lower())
    phrases = r.get_ranked_phrases_with_scores() # To get keyword phrases ranked highest to lowest.

    data = {
        'unigrams': [],
        'bigrams': [],
        'trigrams': [],
    }
    for score, phrase in phrases:
        splitted = phrase.split()
        score = round(score, 2)
        length = len(splitted)
        if length == 1:
            data['unigrams'].append((phrase, score))
        elif length == 2:
            data['bigrams'].append((phrase, score))
        elif length == 3:
            data['trigrams'].append((phrase, score))
    return data
