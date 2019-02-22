import os
import shutil
import random
import pickle

from django.conf import settings
from django.db import transaction

from classifier.generic_classifier import GenericClassifier
from classifier.NaiveBayesSKlearn import SKNaiveBayesClassifier
from classifier.models import ClassifierModel


def create_train_test_data(data):
    random.shuffle(data)
    size = len(data)
    one_fourth = int(size/4)
    train = data[one_fourth:]
    test = data[:one_fourth]
    return (train, test)


def create_classifier_model(
        version,
        csv_path,
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

    # check if version already exists
    try:
        ClassifierModel.objects.get(version=version)
        raise Exception("Classifier version {} already exists".format(version))
    except ClassifierModel.DoesNotExist:
        pass

    from helpers.deep import get_processed_data
    data = get_processed_data(csv_path)

    # get train, test data
    train, test = create_train_test_data(data)

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
    testfilename = 'test_data_v-{}.pkl'.format(version)
    filepath = 'model_test_datas/{}'.format(testfilename)
    with open(filepath, 'wb') as f:
        f.write(pickle.dumps(test))
    modelobj.test_file_path = filepath

    return modelobj


def create_and_save_classifier_model(
        version,
        csv_path,
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
    obj = create_classifier_model(version, csv_path, classifier_class)
    obj.save()
    return obj


def is_valid_path(path):
    if not path or not isinstance(path, str):
        return False
    return os.path.exists(path)


@transaction.atomic
def create_pre_computed_model(kwargs):
    path_names = [
        'model_path', 'pca_model_path', 'tfidf_model_path', 'dictionary_path'
    ]
    paths = {x: kwargs.get(x) for x in path_names}

    for k, v in paths.items():
        if not is_valid_path(v):
            print(v)
            print("invalid path for '{}'".format(k))
            return

    model = pickle.load(open(paths['model_path'], 'rb'))
    generic_model = GenericClassifier(model)

    classifier_model = ClassifierModel()
    classifier_model.version = kwargs['model_version']
    classifier_model.set_data(pickle.dumps(generic_model))

    classifier_model.save()

    # now we have the id, create directory and keep data there
    classifier_path = os.path.join(
        settings.CLASSIFIER_DATA_PATH,
        str(classifier_model.id)
    )
    try:
        os.mkdir(classifier_path)
    except FileExistsError:
        pass

    # Now move the files inside classifier path
    for k, path in paths.items():
        shutil.copy2(
            path,
            os.path.join(
                classifier_path,
                # replacing <something>_path to <something>.pkl
                '{}.pkl'.format(k.replace('_path', ''))
            )
        )

    # now set metadata
    classifier_model.metadata = {
        'dictionary_path': 'dictionary.pkl',
        'dimension_reduce': True,
        'pca_model_path': 'pca_model.pkl',
        'tfidf_model_path': 'tfidf_model.pkl'
    }
    classifier_model.save()


def main(*args, **kwargs):
    if not kwargs.get('model_version'):
        print("Version not provided. Provide it as --model_version <version>")
        return

    type = kwargs.get('type')
    if type == 'pre_computed':
        return create_pre_computed_model(kwargs)
    elif type == 'from_csv':
        csv_path = kwargs.get(
            'path',
            '_playground/sample_data/processed_new_data.csv'
        )
        # TODO; check for model name
        version = kwargs['model_version']

        # get data
        classifier_model = create_and_save_classifier_model(version, csv_path)
        print('Classifier {}- {}  created successfully with  test data'.format(
            classifier_model, classifier_model.id
        ))
    else:
        print("Please provide a valid type as --type=pre_computed|from_csv")
        print("Use 'pre_computed' if there is already a sklearn model")
        print("Use 'from_csv' if there model is created from csv")
