post_data = {
    "message": "Clustering is in progress. Use cluster_model_id for data",
    "cluster_model_id": 1
}

get_data = {
    'id': 1,
    'group_id': '10',
    'n_clusters': 5,
    'score': 0.98,
    # TODO: fill in values
    'doc_ids': [],
    'relevant_terms': []
}


def static_data(request, *args, **kwargs):
    if request.method == 'POST':
        return post_data
    elif request.method == 'GET':
        return get_data
