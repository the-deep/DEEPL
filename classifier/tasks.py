import pickle

from django.utils import timezone

from api.helpers import classify_text
from helpers.common import classification_confidence
from classifier.models import ClassifiedDocument, ClassifiedExcerpt

# NOTE: this is for older classifier update, where user inputs recommended
# label for classification, But at present, we have user giving feedback as
# just the classification was userful or not


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


def update_classified_documents_with_classifier(classifier_model):
    """
    Update the existing classified documents and excerpts with the classifier
    """
    classifier = pickle.loads(classifier_model.data)
    print("Updating classified docs ...")
    for doc in ClassifiedDocument.objects.all():
        classified = classify_text(classifier, doc.text)
        doc.classifier = classifier_model
        doc.confidence = classification_confidence(classified)
        doc.classification_label = classified[0][0]
        doc.classification_probabilities = classified
        doc.save()
    print("Updated classified docs ...")
    print("Updating classified excerpts ...")
    for excerpt in ClassifiedExcerpt.objects.all():
        classified = classify_text(classifier, excerpt.text)
        excerpt.classification_label = classified[0][0]
        excerpt.confidence = classification_confidence(classified)
        excerpt.classification_probabilities = classified
        excerpt.save()
    print("Updated classified excerpts ...")
