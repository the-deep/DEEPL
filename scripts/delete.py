# Script to delete a model
import importlib


def main(*args, **kwargs):
    class_name = kwargs.get('class_name')  # of the form <app>.<name>
    model_id = kwargs.get('modlel_id')
    model_version = kwargs.get('model_version')
    if not class_name:
        print("ERROR: class_name missing. Usage: --class_name=<app.model_class_name>")
        return
    if not (model_id or model_version):
        print("ERROR: expected model_id or model_version to be deleted. Usage: --model_id=<id> --model_version=<version>")
        return
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

    if model_id:
        try:
            model = model_class.objects.get(id=model_id)
        except model_class.DoesNotExist:
            print("ERROR: Model with id {} does not exist".format(model_id))
    elif model_version:
        try:
            model = model_class.objects.get(version=model_version)
        except model_class.DoesNotExist:
            print("ERROR: Model with version {} does not exist".
                  format(model_version))
            return
    try:
        print("Trying to delete model...")
        model.delete()
    except Exception as e:
        print("ERROR while deleting requested model. {}".format(e))
        return
    print("Successfully deleted the requested model")
