import json
import os
import csv

c = 0
c1 = 0


def flat_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for i in x:
                if len(i) < 30:
                    flatten(x[i], name + i + '_')
        elif type(x) is list:
            id = 0
            for i in x:
                if len(i) < 30:
                    flatten(i, name + str(id) + '_')
                    id += 1
        else:
            if type(x) is str:
                x = x[:1000]
            out[name[:-1]] = x  # remove last _

    flatten(y)
    return out


def write_columns(cols):
    file = open('testfile.txt', 'w')
    file.write(", ".join([x for x in cols]))


def read_columns():
    file = open('testfile.txt', 'r')
    cols = file.read()
    cols = cols.split(", ")
    return cols


def extract_val(j_dict):
    global c
    vals = flat_json(j_dict)
    columns = vals.keys()

    if c == 0:
        write_columns(set(columns))
        # print(len(set(columns)))
    else:
        cols = read_columns()
        # print(len(columns))
        columns = list(set(cols) | set(columns))
        print(len(columns))
        write_columns(columns)


def write_val():
    columns = read_columns()
    for file in os.listdir('raw'):
        filename = os.fsdecode(file)
        if filename.endswith(".chlsj"):
            file = open("raw/" + filename, "r")
            vals = flat_json(json.load(file))
            write_csv(columns, vals)


def wrapper():
    for file in os.listdir('raw'):
        filename = os.fsdecode(file)
        if filename.endswith(".chlsj"):
            file = open("raw/" + filename, "r")
            extract_val(json.load(file))
    write_val()


def write_csv(columns, vals):
    global c1
    with open('data/parsed.csv', 'a') as out_file:
        w = csv.DictWriter(out_file, columns)
        if c1 == 0:
            c1 += 1
            w.writeheader()
        w.writerow(vals)
    print("CSV " , read_csv())


def read_csv():

    with open('data/parsed.csv', mode='r') as infile:
        csv_reader = csv.reader(infile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(", ".join(row))
                # print(len(row))
                line_count += 1
            else:
                line_count += 1
    return len(row)


wrapper()
# extract_val()
