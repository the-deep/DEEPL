import unittest
import pytest

from classifier.models import ClassifierModel
from classifier.NaiveBayesSKlearn import SKNaiveBayesClassifier
from helpers.deep import get_processed_data
from helpers.create_classifier import (
    create_train_test_data,
    create_classifier_model
)

csv_path = 'fixtures/processed_data_for_testing.csv'


def test_get_processed_data():
    data = get_processed_data(csv_path)
    assert type(data) == list, "The resulting data should be a list"
    assert type(data[0]) == tuple, "Should be a tuple"
    assert len(data[0]) == 2, "Tuple size should be 2"


def test_create_train_test_data():
    data = get_processed_data(csv_path)
    train, test = create_train_test_data(data)
    assert len(test) == int(len(data)/4)
    assert len(train) == int(3*len(data)/4)


@pytest.mark.django_db
class TestCreateClassifierModel(unittest.TestCase):
    """
    Test the functionality of create_classier_model function
    """
    def setUp(self):
        # create a dummy ClassifierModel object
        self.classifier_model = ClassifierModel.objects.create(
            version=1,
            data=b"This is just dummy data. PLEASE, DON'T UNPICKLE THIS !!",
            name="Dummy model"
        )
        self.classifier_class = SKNaiveBayesClassifier
        self.data = get_processed_data(csv_path)

    def test_create_duplicate_classifier_model(self):
        try:
            create_classifier_model(
                1, self.data, self.classifier_class
            )
        except Exception as e:
            assert "already exists" in e.args[0].lower()
        else:
            assert False, "Model with same version should not be created"

    def test_valid_classifier_model(self):
        classifier_model = create_classifier_model(
            2, self.data, self.classifier_class
        )
        assert type(classifier_model) == ClassifierModel
        assert classifier_model.id is None
        classifier = classifier_model.classifier
        assert type(classifier) == self.classifier_class
