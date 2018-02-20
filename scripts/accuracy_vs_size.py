import os
import sys
import random
import subprocess
import logging
import json


def get_nth_parent_dir(path, n):
    dirname = os.path.dirname(path)
    if n <= 1:
        return dirname
    return get_nth_parent_dir(dirname, n-1)


abs_path = os.path.abspath(__file__)
base = get_nth_parent_dir(abs_path, 2)
print(base)
# add helpers to path
sys.path.insert(0, base)


from classifier.NaiveBayesSKlearn import SKNaiveBayesClassifier
from helpers.deep import get_deep_data
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

try:
    logger.info('.. GETTING DEEP DATA\n')
    print('.. GETTING DEEP DATA\n')
    deepdata = get_deep_data(debug=False)
    deepdata = list(map(
        lambda x: (SKNaiveBayesClassifier.preprocess(x[0]), x[1]), deepdata
    ))
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
    f = open(filepath, 'w')
    logger.info('.. RUNNING LOOP')
    print('.. RUNNING LOOP')
    while dataset_num <= total:
        random.shuffle(deepdata)
        one_fourth = int(dataset_num/4.0)
        train = deepdata[:dataset_num][one_fourth:]
        test = deepdata[:dataset_num][:one_fourth]
        logger.info('.. dataset_num:{}\n'.format(dataset_num))
        classifier = CLASSIFIER.new(train)
        accuracy = classifier.get_accuracy(test)
        num_accuracy.append((dataset_num, accuracy))
        logger.info('.. accuracy: {}\n'.format(accuracy))
        print('.. accuracy: {}\n'.format(accuracy))

        # f.write('{}:{}\n'.format(dataset_num, accuracy))
        dataset_num += increment
    f.write(json.dumps(num_accuracy, indent=2))
    logger.info('.. DONE!!!')
except Exception as e:
    import traceback
    logger.info(traceback.format_exc())
    print(traceback.format_exc())
    logger.info('\n')
finally:
    f.close()
    # logfile.close()
