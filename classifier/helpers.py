import pandas as pd
from classifier.NaiveBayesSKlearn import SKNaiveBayesClassifier

def get_train_test_data(csv_path):
    """csv path points to csv file with sectors and entries"""
    df = pd.read_csv(csv_path)
    processed = df.assign(excerpt=df['excerpt'].apply(
        SKNaiveBayesClassifier.preprocess
    ))
    processed = processed.sample(frac=1)
    l = len(processed)
    one_fourth = int(l/4)
    train = processed['excerpt'][one_fourth:]
    test = processed['excerpt'][:one_fourth]
    target = processed['sector'][one_fourth:]
    test_target = processed['sector'][:one_fourth]
    return (train, target), (test, test_target)
