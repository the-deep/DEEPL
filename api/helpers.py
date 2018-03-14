import re
from rest_framework.response import Response
from importlib import import_module


def classify_text(classifier, text):
    text = classifier.preprocess(text)
    classified = classifier.classify_as_label_probs(text)
    classified.sort(key=lambda x: x[1], reverse=True)
    return classified


def classify_lead_excerpts(classifier, text):
    """
    Classify deep lead data i.e. classify it as well as its sentences(excerpts)
    """
    begins = [m.start() for m in re.finditer('\.\W+[A-Z0-9]', text)]
    textlen = len(text)
    indices = zip([-1]+begins, begins+[textlen-1])
    return [
        {
            'start_pos': s+1,
            'end_pos': e,
            'classification': classify_text(classifier, text[s+1:e+1])
        } for s, e in indices
    ]


def check_if_test(static_script, *dec_args):
    def actual_decorator(f):
        def wrapper(*args, **kwargs):
            test = args[1].GET.get('test')
            tofilter = args[1].GET.get('filter')
            if test and (test == '1') or (test == 'true'):
                if tofilter and (tofilter == '1') or (tofilter == 'true'):
                    kwargs['filter'] = True
                # try to import static_resposnes
                try:
                    imported = import_module('static_responses.'+static_script)
                    return Response(imported.static_data(*args, **kwargs))
                except (ImportError, ModuleNotFoundError):
                    if 'filter' in kwargs:
                        del kwargs['filter']
                    return f(*args, **kwargs)
            else:
                return f(*args, **kwargs)
        return wrapper
    return actual_decorator
