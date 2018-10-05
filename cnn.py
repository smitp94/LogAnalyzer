import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.text import *
from keras.models import model_from_yaml
import numpy as np
import os


def load_data():
    docs = []
    for file in os.listdir('raw'):
        filename = os.fsdecode(file)
        if filename.endswith(".chlsj"):
            f = open("raw/" + filename, "r")
            text = f.read()
            docs.append(text)

    t = Tokenizer()
    # fit the tokenizer on the documents
    t.fit_on_texts(docs)
    encoded_docs = t.texts_to_matrix(docs, mode='count')
    # print(len(encoded_docs))
    # return

    f_test = open("data/FXM_programming will resume.chlsj", "r")  # test data here!!!
    text_test = f_test.read()
    docs_test = [text_test]
    t1 = Tokenizer()
    t1.fit_on_texts(docs_test)
    encoded_test_docs = t1.texts_to_matrix(docs_test, mode='count')

    return (encoded_docs, [0, 0, 1, 0, 0, 0, 0, 1, 0, 1]), (encoded_test_docs, [0]), len(t.word_index), t.word_index


def test():

    (train_data, train_labels), (test_data, test_labels), vocab_size, word_index = load_data()
    # print("Training entries: {}, labels: {}".format(len(train_data), len(train_labels)))
    #
    # print((train_data))
    # return
    # word_index = # above load_data()

    # The first indices are reserved
    word_index = {k: (v + 3) for k, v in word_index.items()}
    word_index["<PAD>"] = 0
    word_index["<START>"] = 1
    word_index["<UNK>"] = 2
    word_index["<UNUSED>"] = 3

    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 16))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(16, activation=tf.nn.relu))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

    train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"], padding='post', maxlen=256)

    test_data = keras.preprocessing.sequence.pad_sequences(test_data, value=word_index["<PAD>"], padding='post', maxlen=256)

    # print(model.summary())

    model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # later for large training set!!!
    # x_val = train_data[:10000]
    # partial_x_train = train_data[10000:]
    #
    # y_val = train_labels[:10000]
    # partial_y_train = train_labels[10000:]
    #
    # history = model.fit(partial_x_train, partial_y_train, epochs=40, batch_size=512, validation_data=(x_val, y_val), verbose=1)

    results = model.evaluate(test_data, test_labels)
    # save_model(model)
    print(results)


def save_model(model):
    # serialize model to YAML
    model_yaml = model.to_yaml()
    with open("model.yaml", "w") as yaml_file:
        yaml_file.write(model_yaml)
    # serialize weights to HDF5
    model.save_weights("model.h5")


def load_model(model):
    # load YAML and create model
    yaml_file = open('model.yaml', 'r')
    loaded_model_yaml = yaml_file.read()
    yaml_file.close()
    loaded_model = model_from_yaml(loaded_model_yaml)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    return loaded_model


test()
