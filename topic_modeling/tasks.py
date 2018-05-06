from celery import task

from topic_modeling.lda import get_topics_and_subtopics
from topic_modeling.models import TopicModelingModel


@task
def get_topics_and_subtopics_task(
        docs, num_topics, kws_per_topic, depth, group_id
        ):
    # topic_model object should have been created
    topic_model = TopicModelingModel.objects.get(group_id=group_id)
    topic_model_data = get_topics_and_subtopics(
        docs, num_topics, kws_per_topic, depth
    )
    topic_model.data = topic_model_data
    topic_model.ready = True
    topic_model.save()
