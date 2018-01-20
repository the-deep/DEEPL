import uuid

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

from classifier.models import BaseModel


class Correlation(BaseModel):
    """Model to store correlation data"""
    correlated_entity = models.CharField(max_length=100) # What is being correlated, eg: topics or subtopics
    version = models.CharField(max_length=20)
    correlation_data = JSONField()

    def __str__(self):
        return '{} Corrlation V{}'.format(self.correlated_entity, self.version)
