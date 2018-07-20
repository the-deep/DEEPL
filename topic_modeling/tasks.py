from celery import task
from django.utils import timezone

from topic_modeling.lda import LDAModel
from topic_modeling.models import TopicModelingModel
from classifier.models import ClassifiedDocument

import logging

logger = logging.getLogger(__name__)


@task
def get_topics_and_subtopics_task(
        group_id, num_topics=5, kws_per_topic=5, depth=1
        ):
    # topic_model object should have been created, at this point
    # but just in case not created, create one
    docs_filter_criteria = {'group_id': group_id}
    try:
        topic_model = TopicModelingModel.objects.get(
            group_id=group_id,
            number_of_topics=num_topics,
            keywords_per_topic=kws_per_topic,
            depth=depth
        )
        if topic_model.last_run_on:
            docs_filter_criteria['created_on__gte'] = topic_model.last_run_on
    except TopicModelingModel.DoesNotExist:
        topic_model = TopicModelingModel.objects.create(
            group_id=group_id,
            number_of_topics=num_topics,
            keywords_per_topic=kws_per_topic,
            depth=depth
        )
    # get classified docs, because model is just created
    docs_qs = ClassifiedDocument.objects.filter(**docs_filter_criteria).\
        values('id', 'group_id', 'text')

    if docs_qs.count() < num_topics:
        return True

    topic_model.ready = False
    topic_model.save()

    # But the algorithm is to be run on all docs, although we checked
    # if new docs added or not
    docs = [x['text'] for x in
            ClassifiedDocument.objects.all().values('id', 'group_id', 'text')]

    lda_model = LDAModel()
    topic_model_data = lda_model.get_topics_and_subtopics(
        docs, num_topics, kws_per_topic, depth
    )
    topic_model.data = topic_model_data
    topic_model.ready = True
    topic_model.last_run_on = timezone.now().date()
    if depth == 1:
        # correlation is relevant only of depth is 1
        topic_model.extra_info = {
            'topics_correlation': lda_model.get_topics_correlation(
                docs, num_topics, kws_per_topic
            )
        }
    topic_model.save()
    return True


@task
def get_topics_task():
    # TODO: figure out about the values
    num_topics = 5
    kws_per_topic = 5
    for x in ClassifiedDocument.objects.values('group_id').distinct():
        gid = x['group_id']
        if gid:
            get_topics_and_subtopics_task(gid, num_topics, kws_per_topic, 1)
    return True
