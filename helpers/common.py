import nltk
import string
import re
import langid
import googletrans
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

from functools import reduce


def tokenize(doc):
    return doc.split()


def compose(*functions):
    def compose2(f1, f2):
        """Compose two functions"""
        return lambda *args: f1(f2(*args))
    return reduce(compose2, functions)


def curry2(func):
    """Curry function with two arguments"""
    return lambda x: lambda y: func(x, y)


def remove_punc_and_nums(input):
    """remove punctuations and replace numbers"""
    punc = string.punctuation
    punc = punc.replace('-', '')
    transtable = str.maketrans("", "", punc)
    punc_removed = input.translate(transtable)
    return re.sub('[0-9]+', 'NN', punc_removed)


def rm_punc_not_nums_list(strlist):
    return list(map(rm_punc_not_nums, strlist))


def rm_stop_words_txt_list(strlist):
    return list(map(rm_stop_words_txt, strlist))


def rm_punc_not_nums(inp, col=None):
    """Remove punctuation unless it's a number for either a df (and col)
    or single entry
    """
    punc = string.punctuation
    transtable = str.maketrans("", "", punc)

    def sing_rm(phr):
        """Remove for a single entity"""
        return ' '.join([re.sub('\W+', '', i).translate(transtable) if not (
                    all(j.isdigit() or j in punc for j in i)
                    and
                    any(j.isdigit() for j in i)
                ) else re.sub('\W+', '', i)
                for i in str(phr).split(' ')]
        )
    if col and isinstance(inp, pd.core.frame.DataFrame):
        return inp.filter(like=col).applymap(lambda phr: sing_rm(phr))
    elif isinstance(inp, str):
        return sing_rm(inp)
    else:
        raise Exception('Not a vaild type')


def rm_stop_words_txt(txt, swords=nltk.corpus.stopwords.words('english')):
    """ Remove stop words from given text """
    return ' '.join(
        [token for token in str(txt).split(' ')
            if token.lower() not in swords]
    )


def rm_stop_words_df(df, col, swords=nltk.corpus.stopwords.words('english')):
    """Remove stop words from a given column in a dataframe"""
    return df.filter(like=col).applymap(
            lambda ent: ' '.join(
                [token for token in str(ent).split(' ')
                    if token.lower() not in swords]
                )
    )


def translate_to_english_txt(text):
    try:
        if langid.classify(text)[0] != 'en':
            trans = googletrans.client.Translator()
            return trans.translate(text, 'en').text
        return text
    except Exception as e:
        return ''


def translate_to_english_df(text):
    return df.filter(like=text).applymap(translate_to_english_txt)


def get_freq_words(words_list):
    """
    Return nltk.FreqDist from given data
    """
    return nltk.FreqDist(w.lower() for w in words_list)


nltk_wordnet_tag_map = {
    'NN': wn.NOUN,
    'NNS': wn.NOUN,
    'VBP': wn.VERB,
    'VBG': wn.VERB,
    'JJ': wn.ADJ,
}


def lemmatize(text, lemmatizer=WordNetLemmatizer()):
    splitted = text if type(text) == list else str(text).split()
    splitted = list(map(lambda x: str(x).lower(), splitted))
    tagged = nltk.pos_tag(splitted)
    lemmatized = []
    for word, tag in tagged:
        wnet_tag = nltk_wordnet_tag_map.get(tag)
        if wnet_tag:
            lemmatized.append(lemmatizer.lemmatize(word, wnet_tag))
        else:
            lemmatized.append(word)
    return ' '.join(lemmatized)


def preprocess(inp, ignore_numbers=False):
    """Preprocess the input string"""
    func = compose(
        ' '.join,
        str.split,
        lemmatize,
        rm_stop_words_txt,
        str.lower,
        remove_punc_and_nums,
        str
    )
    processed = func(inp)
    if ignore_numbers:
        return processed.replace('nn', '')
    return processed


def get_confidence_interval_discrete(percent, true, total):
    factor = 2 if percent == 95 else 1.5  # TODO: add other confidence levels
    adjusted_true = true + 2
    adjusted_total = total + 4
    prob = adjusted_true/float(adjusted_total)
    var = prob * (1-prob)
    err = var/adjusted_total
    sqrt = err**0.5
    error_margin = sqrt*factor
    return (prob-error_margin, prob+error_margin)


def get_n_largest(n, lst, to_compare=lambda x: x):
    """
    This returns largest n elements from list in descending order
    """
    largests = [lst[0]]*n  # this will be in descending order
    for x in lst[1:]:
        if to_compare(x) <= to_compare(largests[-1]):
            continue
        else:
            for i, y in enumerate(largests):
                if to_compare(x) >= to_compare(y):
                    largests = largests[:i] + [x] + largests[i:-1]
                    break
    return largests


def classification_confidence(classification_probabilities):
    """
    Return the classification confidence based on the probabilities.
    @classification_probabilities: [(label, probability)]
    """
    MIN_CONFIDENCE = 0.01
    probs = classification_probabilities
    numclasses = len(probs)
    numrev = 1./numclasses
    maxprob = sorted(probs, key=lambda x: x[1], reverse=True)[0][1]
    return (maxprob - numrev)/(1. - numrev) or MIN_CONFIDENCE


def get_keywords_from_docs(docs):
    """
    @docs: [<tokenized texts> ... ]
    Returns the relevant keywords
    """
    pass


if __name__ == '__main__':
    import pandas as pd
    excerpt = 'Humanitarian needs are said to include access to a sufficient supply of quality water, education, shelter, child protection, health, and nutrition. '
    data = {'excerpt': [excerpt]}
    df = pd.DataFrame(data)
    punc_removed = rm_punc_not_nums(df, 'excerpt')
    stop_removed = rm_stop_words_df(df, 'excerpt')
    print(stop_removed)
