from django.db import models
from django.contrib.postgres.fields import JSONField

from classifier.models import BaseModel


class TopicModelingModel(BaseModel):
    """
    Model storing topic modeling data
    """
    group_id = models.CharField(max_length=50, unique=True)
    data = JSONField(default={})
    number_of_topics = models.IntegerField()
    keywords_per_topic = models.IntegerField()
    depth = models.IntegerField()
    ready = models.BooleanField(default=False)
    extra_info = JSONField(default={})
    last_run_on = models.DateField(null=True)

    def __str__(self):
        return self.group_id
