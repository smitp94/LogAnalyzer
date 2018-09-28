import os
import csv
import re


def file_convert():
    for file in os.listdir('raw'):  # convert raw file to json format
        command = '/Applications/Charles.app/Contents/MacOS/Charles convert \'raw/' + file + '\' \'raw/' + file.rsplit('.', 1)[0] + '.chlsj\''
        os.system(command)


def write_train():
    train = {}
    for file in os.listdir('raw'):  # after converting file to json
        if file.endswith(".chlsj"):
            train[file] = 'yes'

    with open('training_data/train_data.csv', mode='w') as train_file:
        fieldnames = ['file_name', 'bug_name', 'bug']
        data_writer = csv.DictWriter(train_file, fieldnames=fieldnames)
        data_writer.writeheader()
        for file in train:
            data_writer.writerow({'file_name': file, 'bug_name': re.split('[ _]', file, 1)[0], 'bug': train[file]})


# write_train()
file_convert()
