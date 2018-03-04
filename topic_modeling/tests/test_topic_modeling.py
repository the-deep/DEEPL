# import unittest

from topic_modeling.lda import get_topics_and_subtopics


def test_get_topics_and_subtopics():
    """Test the function get_topics and subtopics"""
    documents = [
        "Exercise is good for health",
        "An apple a day keeps the doctor away",
        "Early to bed and early to rise makes a man healthy, wealthy and wise",
    ]
    # Test for 3 topics, 3 words and depth 2 only, this should cover the cases
    num_topics = 3
    depth = 2
    keywords_per_topic = 3
    data = get_topics_and_subtopics(
        documents, num_topics, keywords_per_topic, depth
    )
    for name, topic in data.items():
        assert 'keywords' in topic
        assert isinstance(topic['keywords'], list)
        for kw in topic['keywords']:
            assert isinstance(kw, tuple)
            assert len(kw) == 2
            assert isinstance(kw[0], str)
            assert isinstance(kw[1], int) or isinstance(kw[1], float)
        assert 'subtopics' in topic
        sdata = topic['subtopics']
        assert isinstance(sdata, dict)
        if len(sdata.keys()) == num_topics:
            depth2 = True
            for name, topic in sdata.items():
                assert 'keywords' in topic
                assert isinstance(topic['keywords'], list)
                for kw in topic['keywords']:
                    assert isinstance(kw, tuple)
                    assert len(kw) == 2
                    assert isinstance(kw[0], str)
                    assert isinstance(kw[1], int) or\
                        isinstance(kw[1], float)
                assert 'subtopics' in topic
    assert depth2, "At least one topic should have depth 2"
