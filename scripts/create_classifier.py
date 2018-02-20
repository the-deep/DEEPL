import random
import pickle
import pandas as pd

from classifier.NaiveBayesSKlearn import SKNaiveBayesClassifier
from classifier.models import ClassifierModel


def get_processed_data(csv_file_path):
    """
    return processed_data [(text, label), ... ] from csv file
    NOTE: the processed data should be csv with fields excerpt and sector
    """
    df = pd.read_csv(csv_file_path)
    punc_nums_preprocessor = SKNaiveBayesClassifier.preprocess
    processed = df.assign(excerpt=df['excerpt'].apply(punc_nums_preprocessor))
    excerpts = processed['excerpt']
    sector_labels = processed['sector']
    return list(zip(excerpts, sector_labels))


def create_classifier_model(
        version,
        data,
        classifier_class=SKNaiveBayesClassifier,
        confusion_matrix=True
        ):
    """
    Create a new classifier object to save to the database

    Parameters
    ----------
    @classifier_class : Classifier class to use to creat model
    @data : labeled data list [(text, classification), ...]
    @version : version of the classifier model
    """
    # first create train and test data
    random.shuffle(data)
    size = len(data)
    one_fourth = int(size/4)
    train = data[one_fourth:]
    test = data[:one_fourth]

    classifier = classifier_class.new(train)
    accuracy = classifier.get_accuracy(test)

    if confusion_matrix:
        classifier.calculate_confusion_matrix(test)

    pickle_data = pickle.dumps(classifier)

    modelobj = ClassifierModel(
        data=pickle_data,
        accuracy=accuracy,
        version=version,
        name=classifier_class.__name__
    )
    return modelobj


def create_and_save_classifier_model(
        version,
        data,
        classifier_class=SKNaiveBayesClassifier,
        confusion_matrix=True
        ):
    """
    Create ClassifierModel instance and then save it

    Parameters
    ----------
    @classifier_class : Classifier class to use to creat model
    @data : labeled data list [(text, classification), ...]
    @version : version of the classifier model
    """
    obj = create_classifier_model(version, data, classifier_class)
    obj.save()
    return obj
