from classifier.NaiveBayesSKlearn import SKNaiveBayesClassifier
from api.helpers import classify_text, classify_lead_excerpts

train_data = [
    ('This is sample text 1', 'class A'),
    ('Some other text', 'class B'),
    ('Classification is a very nice algorithm', 'class A'),
    ('Lighting technicians are responsible for the movement and set up of various pieces of lighting equipment for separation of light', 'class A'),
    ('Select lights and equipment to be used and organize any additional equipment', 'class C'),
    ('he Commonwealth Avenue line was originally served by surface streetcars beginning in 1896 as part of what would later become the Green Line "A"', 'class B'),
]


classifier = SKNaiveBayesClassifier.new(train_data)


def static_data(request, *args, **kwargs):
    deeper = request.POST.get('deeper')
    text = request.POST.get('text')
    classified = classify_text(classifier, request.POST['text'])
    if not text:
        return {}
    if not deeper:
        return {
            'classification': classified,
            'classification_confidence': 0.5
        }
    else:
        # classify excerpts as well
        classification = classify_lead_excerpts(classifier, text)
        for x in classification:
            x['classification_confidence'] = 0.5
        return {
            'classification': classified,
            'classification_confidence': 0.5,
            'excerpts_classification': classification
        }
