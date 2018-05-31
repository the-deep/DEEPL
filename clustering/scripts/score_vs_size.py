from sklearn.metrics import silhouette_score
from django.utils import timezone

from classifier.models import ClassifiedDocument
from clustering.base import ClusteringOptions
from clustering.kmeans_docs import KMeansDocs
from helpers.utils import timeit
from helpers.plot import plot
from .optimal_clusters import find_optimal_clusters


@timeit
def plot_score_vs_size(group_id, num_clusters=5):
    # first find optimal clusters
    n, score = find_optimal_clusters(filter_criteria={'group_id': group_id})
    print(
        "The optimal number of clusters is {} with a score {}".
        format(n, score)
    )
    texts = [
        x['text']
        for x in ClassifiedDocument.
        objects.filter(group_id=group_id).values('id', 'text')
    ]
    start_size = 5
    step_size = 2
    if len(texts) < start_size+0*step_size:  # condition is arbitrary
        print("Too few docs for clustering")
    options = ClusteringOptions(n_clusters=n, store_X=True)
    scores_sizes = []
    for x in range(start_size, len(texts), step_size):
        k_means = KMeansDocs(options)
        kmeans_model = k_means.perform_cluster(texts)
        labels = kmeans_model.model.labels_
        score = silhouette_score(k_means.X, labels, metric='euclidean')
        scores_sizes.append([x, score])
    # Now plot
    options = {
        "x_label": "Number of documents",
        "y_label": "Score of clustering"
    }
    title = "Clustering score vs size plot for group_id {}".format(group_id)
    fig = plot(scores_sizes, title, options)
    fig.savefig(
        "Score_vs_size_Group_id_{}__{}.png".
        format(group_id, timezone.now())
    )


def main(*args, **kwargs):
    group_id = kwargs.get('group_id')
    if not group_id:
        print('Missing --group_id')
        return
    plot_score_vs_size(group_id)
