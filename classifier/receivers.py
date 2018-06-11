from django.db.models.signals import post_save

from classifier.models import ClassifiedDocument
from clustering.models import ClusteringModel


def update_clustering_model(sender, instance, **kwargs):
    """Receiver  to set all_clustered field of ClusteringModel to false
    whenever a new doc is added to the same group_id
    """
    if not instance.group_id:
        # because if document is not associated to group, no need to update
        return
    ClusteringModel.objects.filter(group_id=instance.group_id).update(
        all_clustered=False
    )


post_save.connect(update_clustering_model, sender=ClassifiedDocument)
