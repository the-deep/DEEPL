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

try:
    print('.. GETTING DEEP DATA')
    deepdata = []#get_deep_data(debug=False)
    print('.. SHUFFLING DEEP DATA')
    random.shuffle(deepdata)

    total = len(deepdata)

    print('.. INITIALIZING DATASETSIZE TO 100')
    dataset_num = 100
    print('.. SETTING SIZE INCREMENT TO 150')
    increment = 150

    # first create dir to store accuracy vs size data
    print('.. CREATING DIRECTORY `DEEP_DATA` FOR STORING DATA')
    dirpath = os.path.join(os.path.expanduser('~'), 'DEEP_DATA')
    subprocess.call(['mkdir', '-p', dirpath])

    filepath = os.path.join(dirpath, 'accuracy_vs_size.txt')
    f = open(filepath, 'w')
    print('.. RUNNING LOOP')
    while dataset_num<=total:
        print('.. dataset_num:', dataset_num)
        classifier, test_data = get_classifier(4, False, False, debug=False)
        accuracy = classifier.get_accuracy(test_data)
        print('.. accuracy:', accuracy)

        f.write('{}:{}\n'.format(dataset_num, accuracy))
        dataset_num += increment
    f.close()
    print('.. DONE!!!')
except:
    import traceback
    print(traceback.format_exc())
    print()
