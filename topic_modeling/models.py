from django.db import models
from django.contrib.postgres.fields import JSONField

from classifier.models import BaseModel


class TopicModelingModel(BaseModel):
    """
    Model storing topic modeling data
    """
    group_id = models.CharField(max_length=50, unique=True)
    data = JSONField(default={})
    ready = models.BooleanField(default=False)
    extra_info = JSONField(default={})

    def __str__(self):
        return self.group_id
