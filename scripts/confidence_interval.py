import random
import pickle

from helpers.common import get_confidence_interval_discrete


def get_sample_data(data, sample_size=1000):
    """
    Get sample from whole dataset
    """
    random.shuffle(data)
    sectors_samples = {}  # to hold samples of all sectors
    samples_counts = {}  # to hold samples count of sectors
    for excerpt, label in data:
        if not samples_counts.get(label):
            samples_counts[label] = 0
        if samples_counts[label] < sample_size:
            sectors_samples[label] = sectors_samples.get(label, []) + [excerpt]
            samples_counts[label] += 1


def calculate_confidence_interval(classifier_model, data, sample_size=1000):
    """
    Calculate and return the confidence interval of different classes
    """
    sectors_samples = get_sample_data(data, sample_size)
    classifier = pickle.loads(classifier_model.data)
    confidences = {}
    for label, entries in sectors_samples.items():
        total_classified = len(entries)
        correct_classified = 0
        for entry in entries:
            classified = classifier.classify(classifier.preprocess(entry))
            if classified == label:
                correct_classified += 1
        confidence95 = get_confidence_interval_discrete(
            95, correct_classified, total_classified
        )
        confidences[label] = confidence95
    return confidences
    # classifier_model.metadata['confidences_95'] = confidences


def calculate_confidence_interval_and_update(
        classifier_model,
        data,
        sample_size=1000
        ):
    """
    Calculate confidence interval and update the model table
    """
    confidences = calculate_confidence_interval(
        classifier_model, data, sample_size
    )
    classifier_model.metadata['confidences_95'] = confidences
    classifier_model.save()
    return classifier_model
