import pickle
import os
from gensim.models.doc2vec import Doc2Vec


from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings

from classifier.models import BaseModel
from helpers.utils import Resource


class ClusteringModel(BaseModel):
    """
    Model to store clustering data
    """
    name = models.CharField(max_length=100)
    group_id = models.CharField(max_length=20, unique=True, editable=False)
    _data = models.BinaryField()
    n_clusters = models.IntegerField()
    extra_info = JSONField(default={})
    silhouette_score = models.FloatField(default=-1.0)

    def set_model(self, modelobj):
        self._data = pickle.dumps(modelobj)

    def get_model(self):
        return pickle.loads(self._data)

    model = property(get_model, set_model)

    def __str__(self):
        return "{} - Group {}".format(self.name, self.group_id)


class Doc2VecModel(BaseModel):
    """
    Model to store data about gensim doc2vec model created
    """
    name = models.CharField(max_length=100)
    group_id = models.CharField(max_length=20, unique=True, editable=False)
    modelpath = models.CharField(max_length=500)

    PATHTYPE_FILE = 'FILE'
    PATHTYPE_URL = 'URL'

    PATHTYPE_CHOICES = (
        (PATHTYPE_FILE, 'File'),
        (PATHTYPE_URL, 'Url')
    )

    pathtype = models.CharField(
        max_length=50,
        choices=PATHTYPE_CHOICES,
        default=PATHTYPE_FILE
    )

    @classmethod
    def new(cls, doc2vecmodel, name, group_id):
        resource = Resource(
            settings.ENVIRON_DOC2VEC_MODELS_LOCATION,
            Resource.DIRECTORY_AND_ENVIRONMENT
        )
        path = resource.get_resource_location()
        doc2vec = cls(
            name=name,
            group_id=group_id,
            modelpath=path
        )
        doc2vec.save()
        filename = 'doc2vec_id_{}'.format(doc2vec.id)
        doc2vec.modelpath = os.path.join(doc2vec.modelpath, filename)
        doc2vec.save()
        # finally save the doc2vec model in a file
        doc2vecmodel.save(doc2vec.modelpath)
        return doc2vec

    @property
    def model(self):
        return Doc2Vec.load(self.modelpath)
