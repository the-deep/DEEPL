from django.db import transaction

from clustering.doc2vec import create_doc2vec_model
from clustering.models import Doc2VecModel


def main(*args, **kwargs):
    modelname = kwargs.get('model_name')
    group_id = kwargs.get('group_id')
    if not modelname:
        print("Model name not provided. Provide it with: --model_name <name>")
        return
    if not group_id:
        print("Group id not provided. Provide it with: --group_id\
<version>")
        return
    model = create_doc2vec_model()
    try:
        with transaction.atomic():
            dbmodel = Doc2VecModel.new(model, modelname, group_id)
            print("Doc2VecModel with group id {} and name {} has been successfully created".format(
                dbmodel.name, dbmodel.version
            ))
    except Exception as e:
        raise e
