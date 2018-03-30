import pickle

from django.db import models
from django.contrib.postgres.fields import JSONField

from classifier.models import BaseModel


class ClusteringModel(BaseModel):
    """
    Model to store clustering data
    """
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20, unique=True, editable=False)
    _data = models.BinaryField()
    n_clusters = models.IntegerField()
    extra_info = JSONField(default={})

    def set_model(self, modelobj):
        self._data = pickle.dumps(modelobj)

    def get_model(self):
        return pickle.loads(self._data)

    model = property(get_model, set_model)

    def __str__(self):
        return "{} - {}".format(self.name, self.version)
