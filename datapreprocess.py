import json
from pprint import pprint
from plot import plot_drive
import os


def parse_plot():
    plots = {}
    for file in os.listdir('data'):
        filename = os.fsdecode(file)
        if filename.endswith(".chlsj"):
            file = open("data/" + filename, "r")
            data = json.load(file)
            plots[filename] = {}
            x = []
            y = []

            for i in range(len(data)):
                # pprint(data[i]['durations']['total']) # 954290681
                if "fox" in data[i]['host'] and data[i]['durations']['response'] is not None and data[i]['durations']['response'] < 100000:  # to remove one big outlier
                    x.append(data[i]['durations']['response'])
                    y.append(data[i]['durations']['total'])

            plots[filename]['x'] = x
            plots[filename]['y'] = y
    pprint(data[3])
    # plot_drive(plots)


def parse():
    for file in os.listdir('data'):
        filename = os.fsdecode(file)
        if filename.endswith(".chlsj"):
            file = open("data/" + filename, "r")
            data = json.load(file)

            for i in range(len(data)):
                if "api2" in data[i]['host'] and data[i]['durations']['total'] is not None and data[i]['durations']['total'] == 2826:
                    pprint(filename)
                    pprint(data[i])
                    print(data[i]['keptAlive'])
'''
269105
245087
None
3532193216
1268284962 => if ms , 14 days...
11086
'''


parse()
# parse_plot()

