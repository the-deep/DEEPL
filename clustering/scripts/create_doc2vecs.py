from django.db import transaction

from clustering.doc2vec import create_doc2vec_model
from clustering.models import Doc2VecModel


def main(*args, **kwargs):
    modelname = kwargs.get('model_name')
    group_id = kwargs.get('group_id')
    vec_size = kwargs.get('vector_size')
    iterations = kwargs.get('iterations')
    if not modelname:
        print("Model name not provided. Provide it with: --model_name <name>")
        return
    if not group_id:
        print("Group id not provided. Provide it with: --group_id\
<version>")
        return
    kwargs = {}
    if vec_size:
        kwargs['size'] = int(vec_size)
    if iterations:
        kwargs['iterations'] = int(iterations)
    model = create_doc2vec_model(**kwargs)
    try:
        with transaction.atomic():
            dbmodel = Doc2VecModel.new(model, modelname, group_id, kwargs)
            print("Doc2VecModel with group id {} and name {} has been successfully created".format(
                dbmodel.name, dbmodel.group_id
            ))
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print("Exception: {}".format(e))
        raise e
