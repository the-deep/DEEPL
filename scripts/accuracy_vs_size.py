import os
import sys
import random
import subprocess

def get_nth_parent_dir(path, n):
    dirname = os.path.dirname(path)
    if n<=1:
        return dirname
    return get_nth_parent_dir(dirname, n-1)

abs_path = os.path.abspath(__file__)
base = get_nth_parent_dir(abs_path, 2)
# add helpers to path
sys.path.insert(0, base)

from helpers.deep import get_classifier, get_deep_data

# CREATE LOGFILE DIR FIRST
logfiledir = os.path.join(os.path.expanduser('~'), 'logs_DEEPL')
subprocess.call(['mkdir', '-p', logfiledir])
logfilepath = os.path.join(logfiledir, 'accuracy_vs_size.log')

logfile = open(logfilepath, 'w')

try:
    logfile.write('.. GETTING DEEP DATA\n')
    deepdata = get_deep_data(debug=False)
    logfile.write('.. SHUFFLING DEEP DATA\n')
    random.shuffle(deepdata)

    total = len(deepdata)

    logfile.write('.. INITIALIZING DATASETSIZE TO 100\n')
    dataset_num = 100
    logfile.write('.. SETTING SIZE INCREMENT TO 150\n')
    increment = 150

    # first create dir to store accuracy vs size data
    logfile.write('.. CREATING DIRECTORY `DEEP_DATA` FOR STORING DATA\n')
    dirpath = os.path.join(os.path.expanduser('~'), 'data_DEEPL')
    subprocess.call(['mkdir', '-p', dirpath])

    filepath = os.path.join(dirpath, 'accuracy_vs_size.txt')
    f = open(filepath, 'w')
    logfile.write('.. RUNNING LOOP')
    while dataset_num<=total:
        random.shuffle(deepdata)
        logfile.write('.. dataset_num:{}\n'.format(dataset_num))
        classifier, test_data = get_classifier(dataset_num, False, False, debug=False, data=deepdata[:dataset_num])
        accuracy = classifier.get_accuracy(test_data)
        logfile.write('.. accuracy: {}\n'.format(accuracy))

        f.write('{}:{}\n'.format(dataset_num, accuracy))
        dataset_num += increment
    logfile.write('.. DONE!!!')
except:
    import traceback
    logfile.write(traceback.format_exc())
    logfile.write('\n')
finally:
    f.close()
    logfile.close()
