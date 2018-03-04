import unittest
import numpy as np

from classifier.NaiveBayesSKlearn import SKNaiveBayesClassifier
from helpers.deep import get_processed_data
from helpers.create_classifier import create_train_test_data


class TestClassifierSKLearn(unittest.TestCase):
    def setUp(self):
        self.test_data = get_processed_data(
            'fixtures/processed_data_for_testing.csv'
        )
        self.train, self.test = create_train_test_data(self.test_data)
        self.classifier = SKNaiveBayesClassifier.new(self.train)
        self.classifier.calculate_confusion_matrix(self.test)

    def test_preprocess_text(self):
        inp = "This is a test String 1. Is it not?"
        processed = self.classifier.preprocess(inp)
        # Check if all lower
        assert processed == processed.lower(), "Should be lower case"
        # Check stop words not present
        assert "is" not in processed, "Stop word should not be present"
        assert "a" not in processed, "Stop word should not be present"
        assert "This" not in processed, "Stop word should not be present"
        assert "this" not in processed, "Stop word should not be present"
        # Check numbers not present, input contains 1 so check nn is present
        assert "nn" in processed, "Numbers should not be present"
        # Check punctuation not present
        assert "." not in processed, "Punctuation should not be present"
        assert "?" not in processed, "Punctuation should not be present"

    def test_classifiy_text(self):
        # Just test the output formats, not the classification results
        inp = "Text to be classified"
        processed = self.classifier.preprocess(inp)
        classification = self.classifier.classify(processed)
        print(type(classification))
        assert type(classification) == np.str_

    def test_classifiy_list(self):
        # Just test the output formats, not the classification results
        inp = ["Text to be classified", "Another to be classified"]
        processed = map(self.classifier.preprocess, inp)
        classification = self.classifier.classify(processed)
        assert type(classification) == np.ndarray
        assert classification.shape[0] >= 1
        assert type(classification[0]) == np.str_

    def test_classify_as_label_probs(self):
        inp = "Text to be classified"
        processed = self.classifier.preprocess(inp)
        classification = self.classifier.classify_as_label_probs(processed)
        assert type(classification) == list, "Should be [(label, prob)]"
        assert type(classification[0]) == tuple, "Should be (label, prob)"
