import matplotlib.pyplot as plt
import numpy as np


def plot_scatter(x, y):
    x = [0 if i is None else i for i in x]
    y = [0 if i is None else i for i in y]
    color = (0,0.5,0.5)
    plt.scatter(x, y, s=np.pi*3, c=color, alpha=0.5)
    plt.title('Scatter plot total time vs response time')
    plt.xlabel('response')
    plt.ylabel('total')
    plt.show()


def plot_drive(plots):
    color = (0, 0.5, 0.5)
    k=0
    for i in plots:
        k+=1
        plt.subplot(len(plots), 1, k)
        plt.scatter(plots[i]['x'], plots[i]['y'], s=np.pi * 3, c=color, alpha=0.5)
        plt.title(i[:-6])
        plt.xlabel('response')
        plt.ylabel('total')
    plt.show()
