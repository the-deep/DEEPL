from django.db import models
from django.contrib.postgres.fields import JSONField
from classifier.models import BaseModel


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
