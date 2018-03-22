import pickle

from .models import ClassifierModel

__classifiers = {}


def init():
    global __classifiers
    __classifiers = {'v'+str(x.version): {
            'classifier': pickle.loads(x.data),
            'classifier_model': x
            }
            for x in ClassifierModel.objects.all()
        }


def get_classifiers():
    return __classifiers
