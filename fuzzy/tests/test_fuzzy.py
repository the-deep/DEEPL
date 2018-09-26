from fuzzy.levenshtein import levenshtein_distance


def test_distances():
    pairs_dists = [
        ("manhattan", "manahaton", 4),
        ("school", "stool", 3),
        ("country", "laundry", 6),
        ("car", "foo", 6),
        ("car", "baz", 4),
        ("nepak", "nepal", 2),
        # TODO: add other words
    ]
    for a, b, d in pairs_dists:
        assert d == levenshtein_distance(a, b)
