import json
from pprint import pprint

with open('data/test.json') as f:
    data = json.load(f)

pprint(data[0])
