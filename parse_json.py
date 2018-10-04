import json
import os
import csv
import tensorflow as tf
from tensorflow.contrib import learn
import pandas as pd
import numpy as np

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
    # print("write : " + str(len(cols)))


def read_columns():
    file = open('testfile.txt', 'r')
    cols = file.read()
    cols = cols.split(", ")
    # print("read : " + str(len(cols)))
    return cols


def extract_val(j_dict):
    global c
    vals = flat_json(j_dict)
    columns = vals.keys()

    if c == 0:
        c += 1
        write_columns(set(columns))
        # print("0: ", len(set(columns)))
    else:
        cols = read_columns()
        # print("not 0", len(columns))
        columns = list(set(columns) | set(cols))
        # print("not 0", len(columns))
        write_columns(columns)


def write_val():
    columns = read_columns()
    for file in os.listdir('raw'):
        filename = os.fsdecode(file)
        if filename.endswith(".chlsj"):
            file = open("raw/" + filename, "r")
            vals = flat_json(json.load(file))
            write_csv(columns, vals)
            break


def wrapper():
    try:
        os.remove('data/parsed.csv')
    except OSError:
        pass

    for file in os.listdir('raw'):
        filename = os.fsdecode(file)
        if filename.endswith(".chlsj"):
            file = open("raw/" + filename, "r")
            extract_val(json.load(file))
            break
    write_val()
    ###
    # read_csv()
    # preprocess()


def write_csv(columns, vals):
    global c1
    with open('data/parsed.csv', 'a') as out_file:

        # for i in vals:
        #     if i not in columns:
        #         # print(i)
        #         break
        w = csv.DictWriter(out_file, delimiter=',', fieldnames = columns)
        # print(columns)
        # if c1 == 0:
        #     c1 += 1
        w.writeheader()
        w.writerow(vals)
    # print("CSV ", read_csv())


def read_csv():

    with open('data/parsed.csv', mode='r') as infile:
        csv_reader = csv.reader(infile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1
    return len(row)


def preprocess():
    columns = read_columns()
    with open('data/preprocess.csv', 'w') as out_file:

        w = csv.DictWriter(out_file, delimiter=',', fieldnames=columns)


def tf_train():
    columns = read_columns()
    df = pd.read_csv("data/parsed.csv")  # ignore headers!
    l = pd.read_csv("data/label.csv")
    d = df.values
    labels = l.values
    data = np.float32(d if isinstance(d, str) == True else len(d))
    labels = np.array(l)
    x = tf.placeholder(tf.float32, shape=(1, len(columns)))
    x = data
    w = tf.random_normal([100, 150], mean=0.0, stddev=1.0, dtype=tf.float32)  # weight init
    y = tf.nn.softmax(tf.matmul(w, x))

    with tf.Session() as sess:
        print(sess.run(y))

    # filenames = tf.train.string_input_producer(["data/parsed.csv"])
    #
    # # reader = tf.TextLineReader()
    # # key, value = reader.read(filename_queue)
    #
    # record_defaults = len(columns)*[[0.0]]    # setting defaults to 0 initially
    # # cols = tf.decode_csv(
    # #     value, record_defaults=record_defaults)
    # dataset = tf.contrib.data.CsvDataset(filenames, record_defaults)
    # # features = tf.stack(dataset)
    # #
    # # print(features)
    #
    # with tf.Session() as sess:
    #     # Start populating the filename queue.
    #     coord = tf.train.Coordinator()
    #     threads = tf.train.start_queue_runners(coord=coord)


def tf_blind():
    for file in os.listdir('raw'):
        filename = os.fsdecode(file)
        if filename.endswith(".chlsj"):
            file = list(open("raw/" + filename, "r"))
            # extract_val(json.load(file))
            x_text = [sent for sent in file]
            positive_labels = [[0, 1] for _ in file]
            y_test = [1, 0]
            vocab_processor = learn.preprocessing.VocabularyProcessor.restore()
            x_test = np.array(list(vocab_processor.transform(x_text)))


            break

# wrapper()
# extract_val()
tf_train()


# l = 5*[[1]]
# l2= [[1], [1], [1], [1], [1]]
# print(l)
# print(l2)
