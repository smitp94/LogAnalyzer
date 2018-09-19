import json
from pprint import pprint
from plot import plot_scatter
import os


def parse():
    plots = {}
    for file in os.listdir('data'):
            filename = os.fsdecode(file)
            if filename.endswith(".chlsj"):
                file = open("data/" + filename, "r")
                data = json.load(file)
                plots[filename] = {x: '', y: ''}
                x = []
                y = []

                for i in range(len(data)):
                    # pprint(data[i]['durations']['response'])

                    if data[i]['durations']['total'] is not None and data[i]['durations']['total'] < 100000: # to remove one big outlier
                        x.append(data[i]['durations']['response'])
                        y.append(data[i]['durations']['total'])

                plot_scatter(x, y)


parse()
# date, date-time
