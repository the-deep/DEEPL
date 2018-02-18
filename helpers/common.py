import nltk
import string
import re
import langid
import googletrans
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

from functools import reduce


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
    splitted = text if type(text) == list else text.split()
    tagged = nltk.pos_tag(splitted)
    lemmatized = []
    for word, tag in tagged:
        wnet_tag = nltk_wordnet_tag_map.get(tag)
        if wnet_tag:
            lemmatized.append(lemmatizer.lemmatize(word, wnet_tag))
        else:
            lemmatized.append(word)
    return ' '.join(lemmatized)


if __name__ == '__main__':
    import pandas as pd
    excerpt = 'Humanitarian needs are said to include access to a sufficient supply of quality water, education, shelter, child protection, health, and nutrition. '
    data = {'excerpt': [excerpt]}
    df = pd.DataFrame(data)
    punc_removed = rm_punc_not_nums(df, 'excerpt')
    stop_removed = rm_stop_words_df(df, 'excerpt')
    print(stop_removed)
