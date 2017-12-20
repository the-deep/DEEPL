import re

def classify_text(classifier, text):
    classified = classifier.classify_as_label_probs(text.split())
    classified.sort(key=lambda x: x[1], reverse=True)
    return classified

def classify_lead_excerpts(classifier, text):
    """
    Classify deep lead data. i.e. classify it as well as its sentences(excerpts)
    """
    begins = [m.start() for m in re.finditer('\.\W+[A-Z0-9]', text)]
    textlen = len(text)
    indices = zip([-1]+begins, begins+[textlen-1])
    return [
        {
            'start_pos': s+1,
            'end_pos': e,
            'classification': classify_text(classifier, text[s+1:e+1])
        } for s, e in indices
    ]
