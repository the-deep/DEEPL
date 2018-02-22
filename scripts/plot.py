import matplotlib.pyplot as plt
import numpy as np
import datetime
from scipy.interpolate import spline
from scipy import ndimage




COLORS = [
    '#73926e',
    '#e6194b',
    '#3cb44b',
    '#ffe119',
    '#0082c8',
    '#f58231',
    '#911eb4',
    '#aaffc3',
    '#d2f53c',
    '#008080',
    '#e6beff',
    '#aa6e28',
    '#800000',
    '#808080',
]


def plot(data, title=""):
    x = list(map(lambda x: x[0], data))
    y = list(map(lambda x: x[1], data))
    fig = plt.figure(figsize=(15, 8))
    plt.xticks([x for x in range(500, 28000, 1500)])
    plt.xlabel('# of TRAINING SETS')
    plt.ylabel('ACCURACY')
    plt.grid(True)
    plt.plot(x, y, 'k')
    fig.savefig(str(datetime.datetime.now())+".png")


def plot_multiple(data_dict, title=""):
    colorind = 0
    fig = plt.figure(figsize=(15, 8))
    for k, data in data_dict.items():
        x = list(map(lambda x: x[0], data))
        y = list(map(lambda x: x[1], data))

        sigma = 3
        x_g1d = ndimage.gaussian_filter1d(x, sigma)
        y_g1d = ndimage.gaussian_filter1d(y, sigma)
        plt.plot(x_g1d, y_g1d, color=COLORS[colorind], label=k)

        plt.legend()
        colorind += 1
        if colorind >= len(COLORS):
            colorind = 0
    return fig
    fig.savefig(str(datetime.datetime.now())+"_multiple.png")


if __name__ == '__main__':
    import json
    data = json.load(open('accuracy_vs_sizeplotfix_all.json', 'r'))
    overall = data['overall']
    fig = plot_multiple(data['sectors'])
    x = list(map(lambda x: x[0], overall))
    y = list(map(lambda x: x[1], overall))
    sigma = 1.5
    x_g1d = ndimage.gaussian_filter1d(x, sigma)
    y_g1d = ndimage.gaussian_filter1d(y, sigma)
    plt.plot(x_g1d, y_g1d, color='black', label='OVERALL', linewidth=2.5)
    plt.legend(prop={'size': 8})
    plt.xlabel('# of TRAINING SETS')
    plt.ylabel('ACCURACY')
    fig.savefig(str(datetime.datetime.now())+"_multiple.png")
