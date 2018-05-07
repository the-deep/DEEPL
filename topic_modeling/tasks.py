from celery import task

from topic_modeling.lda import get_topics_and_subtopics
from topic_modeling.models import TopicModelingModel
from classifier.models import ClassifiedDocument


@task
def get_topics_and_subtopics_task(
        group_id, num_topics, kws_per_topic, depth
        ):
    # get classified docs
    docs_qs = ClassifiedDocument.objects.filter(group_id=group_id).\
        values('id', 'group_id', 'text')

    docs = list(map(lambda x: x['text'], docs_qs))

    # topic_model object should have been created, at this point
    topic_model = TopicModelingModel.objects.get(
        group_id=group_id,
        number_of_topics=num_topics,
        keywords_per_topic=kws_per_topic,
        depth=depth
    )
    topic_model_data = get_topics_and_subtopics(
        docs, num_topics, kws_per_topic, depth
    )
    topic_model.data = topic_model_data
    topic_model.ready = True
    topic_model.save()
