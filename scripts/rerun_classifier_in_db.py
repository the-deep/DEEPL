import pickle

from classifier.models import (
    ClassifiedDocument, ClassifierModel
)
from helpers.common import classification_confidence


def main(*args):
    classifier_models = ClassifierModel.objects.all()
    classifiers_map = {c.id: pickle.loads(c.data) for c in classifier_models}
    # first run for ClassifiedDocuments
    chunksize = 20
    chunkcounter = 0
    while True:
        frm = chunkcounter * chunksize
        to = (chunkcounter + 1) * chunksize
        objs = ClassifiedDocument.objects.all()[frm:to]
        if not objs:
            print("No more data")
            break
        for doc in objs:
            print('chunk number', chunkcounter, 'doc_id', doc.id)
            prev = doc.classification_probabilities[0]
            classifier = classifiers_map.get(doc.classifier.id)
            if not classifier:
                continue
            processed = classifier.preprocess(doc.text)
            classification_probs = classifier.classify_as_label_probs(processed)
            classification_label = classification_probs[0][0]
            confidence = classification_confidence(classification_probs)
            # update
            doc.classification_label = classification_label
            doc.confidence = confidence
            doc.classification_probabilities = classification_probs
            doc.save()
            print("prev", prev, "current", classification_probs[0])

            # now the excerpts
            for excerpt in doc.excerpts.all():
                txt = processed[excerpt.start_pos:excerpt.end_pos+1]
                classification_probs = classifier.classify_as_label_probs(txt)
                classification_label = classification_probs[0][0]
                confidence = classification_confidence(classification_probs)
                # update
                excerpt.confidence = confidence
                excerpt.classification_probabilities = classification_probs
                excerpt.classification_label = classification_label
                excerpt.save()
        chunkcounter += 1
