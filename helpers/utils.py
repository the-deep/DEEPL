import os


def merge_lists(la, lb, key=lambda x: x):
    """
    Merge two sorted lists
    @la: first list
    @lb: second list (order doesn't matter though)
    @key: comparison key
    """
    merged = []
    lena, lenb = len(la), len(lb)
    lb_ind, la_ind = 0, 0
    while lb_ind < lenb:
        bval = key(lb[lb_ind])
        while la_ind < lena and key(la[la_ind]) <= bval:
            merged.append(la[la_ind])
            la_ind += 1
        merged.append(lb[lb_ind])
        lb_ind += 1
    # if some left in a
    merged.extend(la[la_ind:])
    return merged


def get_env_path_or_exception(env_var):
    indicespath = os.environ.get(env_var)
    if not indicespath or not os.path.isdir(indicespath):
        raise Exception(
            "Please set the environment variable {} to the \
directory where the index files are stored.".format(env_var)
        )
    return indicespath


if __name__ == '__main__':
    import random
    # do test if merge works fine or not
    for x in range(50000):
        randlen1 = random.randrange(5, 50)
        randlen2 = random.randrange(5, 50)
        randlist1 = [random.randrange(1000) for _ in range(randlen1)]
        randlist2 = [random.randrange(1000) for _ in range(randlen2)]
        merged = randlist1 + randlist2
        assert merge_lists(sorted(randlist1), sorted(randlist2)) ==\
            sorted(merged), "Merging sorted and whole sorted should be same"
