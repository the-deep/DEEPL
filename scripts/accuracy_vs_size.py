import os
import sys
import random
import subprocess
import logging
import json
import matplotlib.pyplot as plt
import datetime


def get_nth_parent_dir(path, n):
    dirname = os.path.dirname(path)
    if n <= 1:
        return dirname
    return get_nth_parent_dir(dirname, n-1)


abs_path = os.path.abspath(__file__)
base = get_nth_parent_dir(abs_path, 2)
# add helpers to path
sys.path.insert(0, base)


from classifier.NaiveBayesSKlearn import SKNaiveBayesClassifier
from helpers.deep import get_deep_data, get_processed_data
CLASSIFIER = SKNaiveBayesClassifier

# CREATE LOGFILE DIR FIRST
logfiledir = os.path.join(os.path.expanduser('~'), 'logs_DEEPL')
subprocess.call(['mkdir', '-p', logfiledir])
logfilepath = os.path.join(logfiledir, 'accuracy_vs_size.log')

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(logfilepath)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

# logfile = open(logfilepath, 'w')

num_accuracy = []

def main(*args, **kwargs):

    try:
        logger.info('.. GETTING DEEP DATA\n')
        print('.. GETTING DEEP DATA\n')
        deepdata = get_processed_data(
            '_playground/sample_data/processed_sectors_subsectors.csv'
        )
        logger.info('.. SHUFFLING DEEP DATA\n')
        print('.. SHUFFLING DEEP DATA\n')
        random.shuffle(deepdata)

        total = len(deepdata)

        logger.info('.. INITIALIZING DATASETSIZE TO 500\n')
        print('.. INITIALIZING DATASETSIZE TO 500\n')
        dataset_num = 500
        logger.info('.. SETTING SIZE INCREMENT TO 150\n')
        print('.. SETTING SIZE INCREMENT TO 150\n')
        increment = 150

        # first create dir to store accuracy vs size data
        logger.info('.. CREATING DIRECTORY `DEEP_DATA` FOR STORING DATA\n')
        print('.. CREATING DIRECTORY `DEEP_DATA` FOR STORING DATA\n')
        dirpath = os.path.join(os.path.expanduser('~'), 'data_DEEPL')
        subprocess.call(['mkdir', '-p', dirpath])

        filepath = os.path.join(dirpath, 'accuracy_vs_size.txt')
        logger.info('.. RUNNING LOOP')
        print('.. RUNNING LOOP')
        sectors_accuracies = {}
        while dataset_num <= total:
            random.shuffle(deepdata)
            one_fourth = int(dataset_num/4.0)
            train = deepdata[:dataset_num][one_fourth:]
            test = deepdata[:dataset_num][:one_fourth]
            logger.info('.. dataset_num:{}\n'.format(dataset_num))
            classifier = CLASSIFIER.new(train)
            classifier.calculate_confusion_matrix(test)

            # calculate accuracy for other
            indices = classifier.confusion_matrix._indices
            matrix = classifier.confusion_matrix._confusion
            if not sectors_accuracies:
                sectors_accuracies = {k: [] for k, v in indices.items()}
            for k, v in indices:
                total = sum(matrix[v])
                correct = matrix[v][v]
                sectors_accuracies[k].append([dataset_num, correct/float(total)])

            accuracy = classifier.get_accuracy(test)
            num_accuracy.append((dataset_num, accuracy))
            logger.info('.. accuracy: {}\n'.format(accuracy))
            print('.. accuracy: {}\n'.format(accuracy))

            dataset_num += increment
        # now plot
        data = num_accuracy
        x = list(map(lambda x: x[0], data))
        y = list(map(lambda x: x[1], data))

        print("$$$$$$$$$$$$$$$$$$$")
        print(data)
        print("$$$$$$$$$$$$$$$$$$$")
        print(sectors_accuracies)
        print("$$$$$$$$$$$$$$$$$$$")

        fig = plt.figure(figsize=(15, 8))
        plt.xticks([x for x in range(500, 28000, 1500)])
        plt.xlabel('# of TRAINING SETS')
        plt.ylabel('ACCURACY')
        plt.grid(True)
        plt.plot(x, y, 'k')
        plt.savefig(str(datetime.datetime.now())+".png")

        logger.info('.. DONE!!!')
    except Exception as e:
        import traceback
        logger.info(traceback.format_exc())
        print(traceback.format_exc())
        logger.info('\n')
