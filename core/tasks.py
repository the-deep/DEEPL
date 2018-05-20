from deepl.celery import app

import logging

logger = logging.getLogger('celery')


@app.task
def test_db():
    from classifier.models import ClassifierModel, ClassifiedDocument
    classifier_model = ClassifierModel.objects.last()
    ClassifiedDocument.objects.create(
        classifier=classifier_model,
        classification_label="test",
    )
