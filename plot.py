import matplotlib.pyplot as plt
import numpy as np


def plot_scatter(x, y):
    x = [0 if i is None else i for i in x]
    y = [0 if i is None else i for i in y]

    plt.scatter(x, y, s=np.pi*3, c=(0,0.5,0.5), alpha=0.5)
    plt.title('Scatter plot total time vs response time')
    plt.xlabel('response')
    plt.ylabel('total')
    plt.show()
