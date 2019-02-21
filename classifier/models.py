import uuid
import re
import os
import base64
import pickle
import logging

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

from helpers.common import classification_confidence


logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    """BaseModel for all other models"""
    idx = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(editable=False)
    modified_on = models.DateTimeField()

    def save(self, *args, **kwargs):
        """Override to upate created_on and modified_on"""
        if not self.id:
            self.created_on = timezone.now()
        self.modified_on = timezone.now()
        return super().save(*args, **kwargs)


class ClassifierModel(BaseModel):
    """
    Model to store classifier specific data.
    This stores pickled data as text
    """
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20, unique=True, editable=False)
    # _data is for storing the pickled classifier object
    _data = models.TextField(db_column='data')
    accuracy = models.FloatField(default=0)
    description = models.TextField()
    test_file_path = models.CharField(max_length=250, null=True)
    metadata = JSONField(default={})

    def set_data(self, data):
        self._data = base64.b64encode(data)

    def get_data(self):
        return base64.b64decode(self._data)

    data = property(get_data, set_data)

    @property
    def classifier(self):
        return pickle.loads(self.data)

    def classify_text(self, text):
        meta = self.metadata
        classified = self.classifier.classify_as_label_probs(
            text, meta, self.id)
        classified.sort(key=lambda x: x[1], reverse=True)
        return classified

    def __str__(self):
        return 'v{}-{}'.format(self.version, self.name)


class ClassifiedDocument(BaseModel):
    """
    Model to store the classified document details(especially for deeper
    """
    classifier = models.ForeignKey(ClassifierModel)
    group_id = models.CharField(max_length=20, blank=True, null=True)
    classification_label = models.CharField(max_length=50)
    confidence = models.FloatField(default=0)
    classification_probabilities = JSONField(default={})
    text = models.TextField()
    extra_info = JSONField(default={})
    migrated = models.BooleanField(default=False)

    @property
    def classification_confidence(self):
        return classification_confidence(self.classification_probabilities)

    @classmethod
    def new(self, text, classifier_model, group_id=None):
        classified = classifier_model.classify_text(text)
        return ClassifiedDocument.objects.create(
            text=text,
            classifier=classifier_model,
            confidence=classified[0][1],
            classification_label=classified[0][0],
            classification_probabilities=classified,
            group_id=group_id
        )

    def create_excerpts(self, text):
        begins = [m.start() for m in re.finditer('\.\W+[A-Z0-9]', text)]
        textlen = len(text)
        indices = zip([-1]+begins, begins+[textlen-1])
        return [
            {
                'start_pos': s+1,
                'end_pos': e,
                'classification': self.classifier.classify_text(text[s+1:e+1])
            } for s, e in indices
        ]

    def __str__(self):
        return '{} {}'.format(self.group_id, self.classification_label)


class ClassifiedExcerpt(BaseModel):
    """
    Model to store classified excerpts from the documents
    """
    classified_document = models.ForeignKey(
        ClassifiedDocument,
        related_name="excerpts"
    )
    start_pos = models.IntegerField()
    end_pos = models.IntegerField()
    classification_label = models.CharField(max_length=50)
    confidence = models.FloatField(default=0)
    classification_probabilities = JSONField(default=[])

    @property
    def text(self):
        return self.classified_document.text[self.start_pos:self.end_pos+1]

    @property
    def classification_confidence(self):
        return classification_confidence(self.classification_probabilities)

    def __str__(self):
        return '{} - {} : {}'.format(
            self.start_pos,
            self.end_pos,
            self.classification_label
        )


class Recommendation(BaseModel):
    classifier = models.ForeignKey(ClassifierModel)
    text = models.TextField()
    # label predicted by classifier
    classification_label = models.CharField(max_length=50)
    useful = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    used_date = models.DateTimeField(default=timezone.now)
    extra_info = JSONField(default={})

    def __str__(self):
        return self.classification_label
