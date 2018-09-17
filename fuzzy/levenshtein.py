from fuzzy.data import country


def levenshtein_distance(a, b):
    alen = len(a)
    blen = len(b)
    distance = [[0 for _ in range(alen+1)] for _ in range(blen+1)]
    for x in range(alen+1):
        distance[0][x] = x
    for y in range(blen+1):
        distance[y][0] = y

    for y in range(1, blen+1):
        for x in range(1, alen+1):
            edit = 2  # for substution
            if a[x-1] == b[y-1]:
                edit = 0
            distance[y][x] = min(
                distance[y-1][x] + 1,  # deletion
                distance[y][x-1] + 1,  # insertion
                distance[y-1][x-1] + edit  # substitution
            )
    return distance[blen][alen]


def most_matching(word, corpus, max=10):
    wlen = len(word)
    word = word.lower()
    matching = [corpus[0]] * max
    matching_dists = [999] * max

    for ref in corpus[1:]:
        dist = levenshtein_distance(word, ref['label'].lower())
        if dist > matching_dists[-1]:
            continue
        elif dist < matching_dists[0]:
            matching_dists = [dist] + matching_dists[:-1]
            matching = [ref] + matching[:-1]
        else:
            # First find where to insert
            # TODO: binary search
            i = 0
            while matching_dists[i] < dist:
                i += 1
            # insert at index i
            matching_dists = matching_dists[:i] + [dist] + matching_dists[i:-1]
            matching = matching[:i] + [ref] + matching[i:-1]
    return [
        {
            **x,
            'similarity': wlen/(matching_dists[i]+wlen)
        } for (i, x) in enumerate(matching)
    ]


def find_matching(word, type):
    if type == 'country':
        corpus = country.get_data()
        matching = most_matching(word, corpus)
    else:
        matching = []
    return matching
