import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.text import *
import numpy as np


def load_data():
    f = open("raw/iOS_UCLA copy.chlsj", "r")
    text = f.read()
    text1 = f.read()
    docs = [text, text1]  # !!!

    t = Tokenizer()
    # fit the tokenizer on the documents
    t.fit_on_texts(docs)

    f_test = open("raw/iOS_UCLA copy.chlsj", "r")
    text_test = f_test.read()
    docs_test = [text_test]
    t1 = Tokenizer()
    t1.fit_on_texts(docs_test)

    # words = set(text_to_word_sequence(text))
    # vocab_size = len(words)
    # result1 = hashing_trick(text, round(vocab_size * 1.3), hash_function='md5')

    return (t.word_index.values(), [0]), (t1.word_index.values(), [0]), len(t.word_index), t.word_index


# load_data()


def test():
    imdb = keras.datasets.imdb

    (train_data, train_labels), (test_data, test_labels), vocab_size, word_index = load_data()
    print("Training entries: {}, labels: {}".format(len(train_data), len(train_labels)))

    # word_index = # above load_data()

    # The first indices are reserved
    word_index = {k: (v + 3) for k, v in word_index.items()}
    word_index["<PAD>"] = 0
    word_index["<START>"] = 1
    word_index["<UNK>"] = 2  # unknown
    word_index["<UNUSED>"] = 3

    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 16))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(16, activation=tf.nn.relu))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

    # later for multiple files!!!
    train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                            value=word_index["<PAD>"],
                                                            padding='post',
                                                            maxlen=256)

    test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                           value=word_index["<PAD>"],
                                                           padding='post',
                                                           maxlen=256)

    # print(model.summary())

    model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    results = model.evaluate(test_data, test_labels)

    print(results)


test()
# (train_data, train_labels), (test_data, test_labels) = load_data()
