from rake_nltk import Rake
from helpers.common import remove_punc_and_nums, lemmatize


def get_key_ngrams(
        document, max_grams=3,
        include_numbers=False, single_letters=False
        ):
    # Uses stopwords for english from NLTK, and all puntuation characters.
    r = Rake()
    # r=Rake(<language>) # To use it in a specific language supported by nltk.
    # If you want to provide your own set of stop words and punctuations to
    # r = Rake(<list of stopwords>, <string of puntuations to ignore>)
    if not include_numbers:
        document = remove_punc_and_nums(document)  # numbers are replaced by NN

    document = document.lower()

    # lemmatize
    document = lemmatize(document)
    r.extract_keywords_from_text(document)

    # To get keyword phrases ranked highest to lowest.
    phrases = r.get_ranked_phrases_with_scores()

    data = {'{}grams'.format(x+1): [] for x in range(max_grams)}

    for score, phrase in phrases:
        if 'NN' in phrase.upper():
            continue
        splitted = phrase.split()
        if any(map(lambda x: len(x) < 3, splitted)):
            continue
        score = round(score, 2)
        length = len(splitted)
        if length <= max_grams:
            data['{}grams'.format(length)].append((phrase, score))
    return data
