import pickle

from django.db.utils import ProgrammingError

from .models import ClassifierModel

__classifiers = {}


def init():
    global __classifiers
    try:
        __classifiers = {'v'+str(x.version): {
                'classifier': pickle.loads(x.data),
                'classifier_model': x
                }
                for x in ClassifierModel.objects.filter(is_active=True)
            }
    except ProgrammingError as e:
        print("PROGRAMMING ERROR: ", e)


def get_classifiers():
    return __classifiers
