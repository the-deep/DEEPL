import random
import pickle

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
        data,
        classifier_class=SKNaiveBayesClassifier,
        confusion_matrix=False
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


def main(*args, **kwargs):
    if not kwargs.get('model_version'):
        print("Version not provided. Provide it as --modelversion <version>")
        return
    # TODO; check for model name
    version = kwargs['model_version']
    csv_path = '_playground/sample_data/processed_new_data.csv'
    # csv_path = '_playground/sample_data/all_en_processed_sectors_subsectors.csv'

    from helpers.deep import get_processed_data

    # get data
    data = get_processed_data(csv_path)
    classifier_model = create_and_save_classifier_model(version, data)
    print('Classifier {}  created successfully with  test data'.format(
        classifier_model
    ))
