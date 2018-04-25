from celery import task


@task
def test_celery():
    import time
    time.sleep(3)
    with open('/tmp/a.log', 'w') as f:
        f.write('bibek pandey')
        f.close()


@task
def test_db():
    from classifier.models import ClassifierModel, ClassifiedDocument
    classifier_model = ClassifierModel.objects.last()
    ClassifiedDocument.objects.create(
        classifier=classifier_model,
        classification_label="test",
    )
