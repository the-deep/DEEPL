import csv
import json
import os
import string
import pandas as pd
import nltk
import googletrans
import langid
import pickle

from django.utils import timezone

from helpers.deep import (
    get_sector_excerpt,
)

def process_deep_entries_data(csv_file_path):
    """
    Take in a csv file consisting of folloing columns:
        'onedim_j', 'twodim_j', 'reliability', 'severity', 'demo_groups_j',
        'specific_needs_j', 'aff_groups_j', 'geo_j', 'info_date', 'excerpt',
        'has_image', 'lead_text', 'lead_id', 'lead_url', 'event'
    Process it(remove stop words, translate language,...)
    And return list of tuples: [(text, label)...]
    """

    df = pd.read_csv(csv_file_path, header = 0)
    # Convert json string columns to json
    df[df.filter(like="_j").columns] = df.filter(like="_j").applymap(
        lambda x : json.loads(x)
    )
    # Change column names
    for v in df.filter(like="_j"):
        df = df.rename(columns = {v : '_'.join(v.split('_')[:-1])})

    # filter texts only if langid english

    return get_sector_excerpt(df)


def update_classifiers():
    from classifier.models import Recommendation
    reccos = Recommendation.objects.filter(is_used=False)
    versions = {}
    versions_recos = {}
    for r in reccos:
        clf = r.classifier
        ver = clf.version
        if not versions.get(ver):
            versions[ver] = clf
        if not versions_recos.get(ver):
            versions_recos[ver] = []
        versions_recos[ver].append(r)
    # Now that we have recommendations for different versions
    for v, recos in versions_recos.items():
        classifier_obj = pickle.loads(versions[v].data)
        new_classifier_obj = classifier_obj.retrain([
            (r.text, r.classification_label)
            for r in recos
        ])
        versions[v].data = pickle.dumps(new_classifier_obj)
        # TODO: might need to update version
        versions[v].save()
        for x in reccos:
            x.is_used = True
            x.used_date = timezone.now()
            x.save()
    return True
