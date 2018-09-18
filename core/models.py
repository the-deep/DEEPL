import uuid

from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import JSONField


class BaseModel(models.Model):
    """
    BaseModel for all other models
    NOTE: There exists another base model but unfortunately abstract=True
    was not set
    """
    idx = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(editable=False)
    modified_on = models.DateTimeField()

    def save(self, *args, **kwargs):
        """Override to upate created_on and modified_on"""
        if not self.id:
            self.created_on = timezone.now()
        self.modified_on = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField(max_length=100)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)

    extra_info = JSONField(default={})

    def __str__(self):
        return self.name
