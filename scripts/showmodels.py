# Script to show model based on filter params
import importlib


# TODO: custom fields, and filters
def main(*args, **kwargs):
    class_name = kwargs.get('class_name')
    if not class_name:
        print("ERROR: class_name missing. Usage: --class_name=<app.model_class_name>")
        return
    filter_kwargs = {}
    try:
        app, modelclass = class_name.split('.')
        # import app models
        m = importlib.import_module('{}.models'.format(app))
        model_class = getattr(m, modelclass)
    except ImportError as e:
        print("ERROR: Can't import '{}.models'".format(app))
        return
    except NameError as e:
        print(e)
        print("ERROR: No such class '{}' in app '{}'".format(modelclass, app))
        return

    try:
        models = model_class.objects.filter(**filter_kwargs)
    except Exception as e:
        print(e)
        return
    else:
        print("MODELS:")
        for model in models:
            print("Id: {}    Name: {}    group_id: {}".format(
                model.id,
                model.name[:20].ljust(20),
                model.group_id[:20].ljust(20),
            ))
