import os
import sys
import random
import subprocess
import logging
import json
import matplotlib.pyplot as plt
import datetime

def plot(data, title=""):
    # data = [(500, 0.47999999999999998), (650, 0.61728395061728392), (800, 0.52000000000000002), (950, 0.54430379746835444), (1100, 0.64727272727272722), (1250, 0.64743589743589747), (1400, 0.58857142857142852), (1550, 0.57105943152454786), (1700, 0.61176470588235299), (1850, 0.62770562770562766), (2000, 0.66400000000000003), (2150, 0.64059590316573556), (2300, 0.60521739130434782), (2450, 0.63888888888888884), (2600, 0.64923076923076928), (2750, 0.65211062590975255), (2900, 0.6441379310344828), (3050, 0.64698162729658792), (3200, 0.64875000000000005), (3350, 0.65710872162485068), (3500, 0.64228571428571424), (3650, 0.65131578947368418), (3800, 0.64315789473684215), (3950, 0.65349544072948329), (4100, 0.67707317073170736), (4250, 0.64500941619585683), (4400, 0.66363636363636369), (4550, 0.66842568161829374), (4700, 0.64851063829787237), (4850, 0.66584158415841588), (5000, 0.66080000000000005), (5150, 0.66744366744366745), (5300, 0.67622641509433967), (5450, 0.68575624082232012), (5600, 0.66428571428571426), (5750, 0.66875434933890043), (5900, 0.68745762711864411), (6050, 0.65740740740740744), (6200, 0.6670967741935484), (6350, 0.66603654694391934), (6500, 0.69846153846153847), (6650, 0.68712394705174484), (6800, 0.67647058823529416), (6950, 0.66666666666666663), (7100, 0.67774647887323947), (7250, 0.66777041942604853), (7400, 0.67297297297297298), (7550, 0.68521462639109698), (7700, 0.67220779220779225), (7850, 0.68807339449541283), (8000, 0.65649999999999997), (8150, 0.68924889543446244), (8300, 0.68385542168674696), (8450, 0.703125), (8600, 0.66279069767441856), (8750, 0.6890717878372199), (8900, 0.69393258426966287), (9050, 0.68258178603006192), (9200, 0.69956521739130439), (9350, 0.68891741548994434), (9500, 0.67621052631578948), (9650, 0.68864013266998336), (9800, 0.66653061224489796), (9950, 0.69280257338158424), (10100, 0.68673267326732679), (10250, 0.68540202966432473), (10400, 0.68538461538461537), (10550, 0.67804323094425478), (10700, 0.691214953271028), (10850, 0.69395280235988199), (11000, 0.68690909090909091), (11150, 0.69573017581628993), (11300, 0.695575221238938), (11450, 0.69426974143955278), (11600, 0.6972413793103448), (11750, 0.69799114742934965), (11900, 0.7038655462184874), (12050, 0.6822709163346613), (12200, 0.69442622950819677), (12350, 0.69679300291545188), (12500, 0.70016), (12650, 0.70904490828589495), (12800, 0.68781250000000005), (12950, 0.70342910101946243), (13100, 0.68793893129770989), (13250, 0.70169082125603865), (13400, 0.69611940298507458), (13550, 0.7032772364924712), (13700, 0.6928467153284672), (13850, 0.70103986135181973), (14000, 0.70485714285714285), (14150, 0.68843652813118461), (14300, 0.70377622377622373), (14450, 0.69352159468438535), (14600, 0.69260273972602737), (14750, 0.69433143477081638), (14900, 0.694496644295302), (15050, 0.69883040935672514), (15200, 0.69973684210526321), (15350, 0.70445660672400312), (15500, 0.69393548387096771), (15650, 0.70398773006134974), (15800, 0.69645569620253167), (15950, 0.69902182091798348), (16100, 0.70708074534161491), (16250, 0.70064007877892664), (16400, 0.70487804878048776)]
    x = list(map(lambda x: x[0], data))
    y = list(map(lambda x: x[1], data))
    fig = plt.figure(figsize=(15, 8))
    plt.xticks([x for x in range(500, 28000, 1500)])
    plt.xlabel('# of TRAINING SETS')
    plt.ylabel('ACCURACY')
    plt.grid(True)
    plt.plot(x, y, 'k')
    plt.savefig(str(datetime.datetime.now())+".png")


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
