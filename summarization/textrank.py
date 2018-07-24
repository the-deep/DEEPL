import numpy as np
from helpers.common import preprocess, text_to_sentences


def page_rank(matrix, epsilon=0.001, d=0.85, max_iter=200):
    """
    @matrix: tranition matrix
    @epsilon: small value which determines if result has been converged
    @d: damping factor
    @max_iter: if not converging well, stop after some iterations
    """
    size = len(matrix)
    ones = np.ones(size)
    curr_prob = ones / size
    d_size = d / size
    one_min_d_size = (1-d)/size
    for x in range(max_iter):
        new_prob = ones * (one_min_d_size) + d_size * matrix.T.dot(curr_prob)
        diff = abs(new_prob - curr_prob).sum()
        if diff <= epsilon:
            break
    # below, negative serves for reverse sort
    return sorted(enumerate(new_prob), key=lambda x: -x[1])


def sentences_similarity(s1, s2):
    s1_splitted = s1.split()
    s2_splitted = s2.split()
    vocab = list(set(s1_splitted + s2_splitted))
    vocab_size = len(vocab)
    # TODO: write the following in same loop for efficiency
    s1_vec = [1. if x in s1_splitted else 0. for x in vocab]
    s2_vec = [1. if x in s2_splitted else 0. for x in vocab]
    return sum([x*y for x, y in zip(s1_vec, s2_vec)]) / (vocab_size*vocab_size)


def text_rank(sentences):
    """
    @sentences: list of sentences
    """
    # first calculate the transition matrix using sentence similarity
    size = len(sentences)
    processed = [preprocess(x) for x in sentences]
    matrix = [[1.0 for _ in range(size)] for _ in range(size)]  # later updated
    for i, s1 in enumerate(sentences):
        for j in range(i+1, size):
            # no need to check for i==j case as it is already set 1.0
            similarity = sentences_similarity(processed[i], processed[j])
            matrix[i][j] = similarity
            matrix[j][i] = similarity
    return page_rank(np.asarray(matrix))


def summarize_text(text, num_sentences=4):
    """
    @text: text to be summarized
    """
    # get sorted sentence_ranks
    sentences = [x.strip() for x in text_to_sentences(text.strip())]
    if len(sentences) < 4:
        return ''
    sentences_rank = text_rank(sentences)
    imp_sentences = sentences_rank[:num_sentences]
    # now we have important sentences, order them as in the original text
    imp_sentences = sorted(imp_sentences, key=lambda x: x[0])
    return '. '.join([sentences[x] for x, _ in imp_sentences])


if __name__ == '__main__':
    matrix = np.asarray([
        [0, 0.33, 0.33, 0, 0.33],
        [0.5, 0, 0, 0.5, 0],
        [0.5, 0, 0, 0, 0.5],
        [0, 0.5, 0, 0, 0.5],
        [0.33, 0, 0.33, 0.33, 0],
    ])

    text = '''
    After having some sleepless nights(I am insomniac sometimes) and re-preparations after the first exam, on the day of second exam, I collected my admit card, pen, pencil, calculator and went to the examination centre in Dhapakhel.
A bit nervous, a bit excited and a bit happy(because I would be free from preparations that day), I reached the exam centre which was Kantipur Engineering College, a beautiful place. I met my friends, excited and happy. We had some talks about how we were quite nervous and excited and how we had prepared for that exam.
    '''
    print(summarize_text(text))
