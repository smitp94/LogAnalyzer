import json
from pprint import pprint
from plot import plot_scatter


with open('data/test.json') as f:
    data = json.load(f)

x = []
y = []
for i in range(len(data)):
    # pprint(data[i]['durations']['response'])
    # pprint(data[i]['durations']['total'])
    if data[i]['durations']['total'] is not None: #and data[i]['durations']['total'] < 100000: # to remove one big outlier
        x.append(data[i]['durations']['response'])
        y.append(data[i]['durations']['total'])
print(len(x))
print(len(y))

plot_scatter(x, y)

# date, date-time
