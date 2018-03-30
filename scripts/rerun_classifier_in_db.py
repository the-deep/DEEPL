import pickle

from classifier.models import (
    ClassifiedDocument, ClassifierModel, ClassifiedExcerpt
)
from helpers.common import classification_confidence

from django.db import transaction


def main(*args, **kwargs):
    classifier_models = ClassifierModel.objects.all()
    classifiers_map = {c.id: pickle.loads(c.data) for c in classifier_models}
    # first run for ClassifiedDocuments
    chunksize = 20
    chunkcounter = 0
    while True:
        frm = chunkcounter * chunksize
        to = (chunkcounter + 1) * chunksize
        texts = ClassifiedDocument.objects.all().\
            values('id', 'text', 'classifier')[frm:to]
        if not texts:
            print("No more data")
            break
        print('RUNNING CHUNK', chunkcounter)

        for x in texts:
            continue
            clf = classifiers_map.get(x['classifier'])
            clfn = clf.classify_as_label_probs(clf.preprocess(x['text']))
            x['classification_probabilities'] = clfn
            x['confidence'] = classification_confidence(clfn)

        # make atomic transaction
        with transaction.atomic():
            for x in texts:
                continue
                probs = x['classification_probabilities']
                ClassifiedDocument.objects.filter(id=x['id']).update(
                    classification_label=probs[0][0],
                    confidence=x['confidence'],
                    classification_probabilities=probs
                )

        # now the excerpts
        for x in texts:
            excerpts = ClassifiedExcerpt.objects.filter(
                classified_document__id=x['id']
            ).values('id', 'start_pos', 'end_pos')
            for y in excerpts:
                print("EXC ID",  y['id'])
                clf = classifiers_map.get(x['classifier'])
                clfn = clf.classify_as_label_probs(clf.preprocess(
                    x['text'][y['start_pos']:y['end_pos']]
                ))
                y['classification_probabilities'] = clfn
                y['confidence'] = classification_confidence(clfn)

            # update the excerpts
            with transaction.atomic():
                for y in excerpts:
                    probs = y['classification_probabilities']
                    ClassifiedExcerpt.objects.filter(id=y['id']).update(
                        classification_label=probs[0][0],
                        classification_probabilities=probs,
                        confidence=y['confidence']
                    )
        chunkcounter += 1
