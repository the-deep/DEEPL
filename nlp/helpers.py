import pandas as pd
import nltk
import string

def rm_punc_not_nums(inp, col=None):
    """remove punctuation unless it's a number for either a df (and col) or single entry"""
    punc =  string.punctuation
    transtable = str.maketrans("","", punc)

    def sing_rm(phr):
        """remove for a single entity"""
        return ' '.join([i.translate(transtable) if not (
                    all(j.isdigit() or j in punc for j in i)
                    and
                    any(j.isdigit() for j in i)
                ) else i
                for i in str(phr).split(' ')]
        )

    if isinstance(inp, pd.core.frame.DataFrame):
        return inp.filter(like=col).applymap(lambda phr : sing_rm(phr))

    elif isinstance(inp, str):
        return sing_rm(inp)

    else:
        raise Exception('Not a vaild type')

def rm_stop_words_txt(txt, swords=nltk.corpus.stopwords.words('english')):
    """ Remove stop words from given text """
    return ' '.join([token for token in str(txt).split(' ') if token.lower() not in swords])

def rm_stop_words_df(df, col, swords = nltk.corpus.stopwords.words('english')):
    """remove stop words from a given column in a dataframe"""
    return df.filter(like=col).applymap(lambda ent:
                    ' '.join([token for token in str(ent).split(' ') if token.lower() not in swords]))

if __name__ == '__main__':
    excerpt = 'Humanitarian needs are said to include access to a sufficient supply of quality water, education, shelter, child protection, health, and nutrition. '
    data = {'excerpt': [excerpt]}
    df = pd.DataFrame(data)
    punc_removed = rm_punc_not_nums(df, 'excerpt')
    stop_removed = rm_stop_words_df(df, 'excerpt')
    print(stop_removed)
