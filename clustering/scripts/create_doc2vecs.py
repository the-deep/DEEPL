from django.db import transaction

from clustering.doc2vec import create_doc2vec_model
from clustering.models import Doc2VecModel


def main(*args, **kwargs):
    modelname = kwargs.get('model_name')
    modelversion = kwargs.get('model_version')
    if not modelname:
        print("Model name not provided. Provide it with: --model_name <name>")
        return
    if not modelversion:
        print("Model version not provided. Provide it with: --model_version\
<version>")
        return
    model = create_doc2vec_model()
    try:
        with transaction.atomic():
            dbmodel = Doc2VecModel.new(model, modelname, modelversion)
            print("Doc2VecModel with version {} and name {} has been successfully created".format(
                dbmodel.name, dbmodel.version
            ))
    except Exception as e:
        raise e
