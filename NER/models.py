import uuid
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from classifier.models import BaseModel, ClassifiedDocument


class GoogleLocationCache(BaseModel):
    _location = models.CharField(max_length=50, unique=True)
    location_info = JSONField()

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = str(value).lower()

    def __str__(self):
        return self.location


class NERCache(models.Model):
    idx = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(editable=False)
    modified_on = models.DateTimeField()
    classified_doc = models.ForeignKey(ClassifiedDocument, unique=True)
    ner_data = JSONField()

    def save(self, *args, **kwargs):
        """Override to upate created_on and modified_on"""
        if not self.id:
            self.created_on = timezone.now()
        self.modified_on = timezone.now()
        return super().save(*args, **kwargs)
