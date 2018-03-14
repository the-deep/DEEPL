import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import random
import math

from helpers.deep import get_processed_data
from helpers.common import classification_confidence


COLORS = [
    '#73926e',
    '#e6194b',
    '#3cb44b',
    '#ffe119',
    '#0082c8',
    '#f58231',
    '#911eb4',
    '#d2f53c',
    '#008080',
    '#e6beff',
    '#aa6e28',
    '#800000',
    '#808080',
]


def get_confidences(classifier, test_data):
    """
    Get the confidences values for all the datasets
    @classifier: classifier object
    @test_data: test data specific to the classifier

    It returns {correct_confidences: [float], incorrect_confidences:[float]}
    """
    # deep_data = get_processed_data(
        # '_playground/sample_data/processed_sectors_subsectors.csv'
        # # 'fixtures/processed_data_for_testing.csv'
    # )
    # confidences for correct and incorrect prediction
    correct_confidences = []
    incorrect_confidences = []

    for text, label in test_data:
        classification = classifier.classify_as_label_probs(text)
        confidence = classification_confidence(classification)
        classified_label = classification[0][0]  # get the max
        if classified_label == label:  # means correct confidence
            correct_confidences.append(confidence)
        else:
            incorrect_confidences.append(confidence)
    print(
            "correct:",
            len(correct_confidences),
            "incorrect:",
            len(incorrect_confidences)
        )
    return {
        'correct_confidences': correct_confidences,
        'incorrect_confidences': incorrect_confidences
    }


def scatter_plot(confidences):
    fig = plt.figure(figsize=(20, 8))
    maxlen = max([len(x) for k, x in confidences.items()])
    for key, confs in confidences.items():
        color = COLORS[random.randrange(len(COLORS))]
        mean = np.mean(confs)
        # median = np.median(confs)
        plt.scatter(np.arange(len(confs)), confs, color=color, label=key, s=5)
        meanX = [x for x in range(maxlen)]
        meanY = [mean for _ in range(maxlen)]
        plt.plot(meanX, meanY, color=color, label="{} mean [{}]".format(
            key, mean))
    plt.legend()
    return fig


def prepare_bar_chart_data(confidence_values, label=''):
    initial_ranges = [round(x*0.05, 2) for x in range(0, 21)]
    zipped = zip(initial_ranges, initial_ranges[1:])
    x_axes = ["{}-{}".format(x[0], x[1]) for x in zipped]
    xvals = np.arange(len(x_axes))
    counts = [0]*len(x_axes)
    for x in confidence_values:
        index = math.ceil(x/0.05) or 1  # can't be 0 else index will be -1
        counts[index-1] += 1
    return {
        'x_axes': x_axes,
        'xvals': xvals,
        'yvals': counts,
        'label': label
    }


def bar_chart(datas):
    fig = plt.figure(figsize=(15, 8))
    for i, data in enumerate(datas):
        plt.bar(
            data['xvals']+i*data['bar_width'],
            data['yvals'],
            data['bar_width'],
            align='center',
            alpha=0.5,
            label=data.get('label', "X")
        )
        plt.ylabel('# Entries')
    plt.xticks(datas[0]['xvals'], data['x_axes'], rotation=30)
    plt.title('Classifier_confidences')
    plt.legend()
    plt.tight_layout()
    return fig


def main(*args):
    import pickle
    import datetime
    from classifier.models import ClassifierModel
    if not args:
        print("ERROR: Please provide model version number.\nUSAGE: ./manage.py runscript classifier_confidence <version number> [scatterplot|bar]")
        return
    pk = args[0]
    c = ClassifierModel.objects.get(version=pk)
    # Get test data
    try:
        testdata = pickle.load(open(c.test_file_path, 'rb'))
    except FileNotFoundError:
        print("ERROR: Test data file could not be found")
        return
    except TypeError:
        print("ERROR: Could not load test data file. Does classifier Model have file path set?")
        return

    classifier = pickle.loads(c.data)
    print("Getting confidences of the latest model")
    confs = get_confidences(classifier, testdata)

    name = '{}-{}.png'.format(datetime.datetime.now(), {})
    name = name.replace(' ', '.')
    if len(args) > 1 and args[1] == 'scatterplot':
        print("Creating scatterplot of the confidences")
        f = scatter_plot(confs)
        name = name.format('scatter')
        f.savefig(name)
    else:  # default is bar
        print("Creating bar chart for the confidences")
        BAR_WIDTH = 0.4
        bardata = prepare_bar_chart_data(
            confs['correct_confidences'],
            'Correct Classifications'
        )
        bardata['label'] = 'Correct classifications'
        bardata['bar_width'] = BAR_WIDTH
        inc_bardata = prepare_bar_chart_data(
            confs['incorrect_confidences'],
            'Incorrect Classifications'
        )
        inc_bardata['bar_width'] = BAR_WIDTH
        f = bar_chart([bardata, inc_bardata])
        name = name.format('bar')
        f.savefig(name)
    print("Saved graph as {}".format(name))
