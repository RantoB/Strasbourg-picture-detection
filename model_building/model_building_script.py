import numpy as np
from numpy.core.defchararray import find
import os
import pickle
import json
import csv
from datetime import datetime as dt
import concurrent.futures

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import tensorflow as tf
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from tensorflow.keras.models import save_model

import logging

import time

logging.basicConfig(level=logging.INFO)

DATA_PATH = '../data'
MODEL_SAVING_PATH = '../Models'

def load_data():
    directory = np.array(os.listdir(DATA_PATH))
    directory = directory[find(directory, '.pkl') != -1]

    # data_path = input('File_name : ')
    data_path = ''

    if data_path == '':

        created_times = list()

        for file in directory:
            data_path = os.path.join(DATA_PATH, file)
            created_times.append(os.stat(data_path).st_ctime_ns)

        created_times = np.array(created_times)

        most_recent_file = directory[np.argmax(created_times)]

        logging.info(f'Most recent_file will be used : {most_recent_file}')

        data_path = os.path.join(DATA_PATH, most_recent_file)

    elif data_path not in directory:
        logging.info(f'no such fill : {data_path}')

    with open(data_path, "rb") as f:
        data = pickle.load(f)

    return data

def train_model(block_number, neurone_number, activation_function):
    data = load_data()

    X_train, X_test, y_train, y_test = train_test_split(data['images'] / 255.,
                                                       data['y'],
                                                       test_size = .1,
                                                        stratify=data['y'])

    number_of_cat = len(np.unique(data['y']))

    y_train_cat = to_categorical(y_train, number_of_cat)
    y_test_cat = to_categorical(y_test, number_of_cat)

    base_model = VGG16(weights=None, include_top=True,
             input_shape=X_train.shape[1:], classes=number_of_cat)

    data_gen = ImageDataGenerator(rotation_range=20, zoom_range=[.7, 1.3], shear_range=5)
    data_gen.fit(X_train)

    callbacks = [EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)]

    x = base_model.get_layer(f'block{block_number}_pool').output
    x = Flatten(name='flatten_layer')(x)
    x = Dense(neurone_number, activation=activation_function)(x)
    x = Dense(number_of_cat, activation='softmax')(x)

    model = Model(inputs=base_model.inputs, outputs=x)

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    epochs = 2 # 50

    # model.fit(X_train, y_train_cat,
    #       validation_data=(X_test, y_test_cat), epochs=epochs,
    #       steps_per_epoch=len(X_train) / 32, callbacks=callbacks)

    model.fit(data_gen.flow(X_train, y_train_cat, batch_size=32),
          validation_data=(X_test, y_test_cat), epochs=epochs,
          steps_per_epoch=len(X_train) / 32, callbacks=callbacks)

    pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, tf.argmax(pred, axis=1))

    return model, accuracy

def save_model_and_results(block_number, neurone_number, activation_function):
    model, accuracy = train_model(block_number, neurone_number, activation_function)
    time_stamp = dt.now()
    time_string = time_stamp.strftime('%H%M%d%m%Y')
    model_name = 'model_' + str(block_number) + str(neurone_number) + activation_function + time_string
    saving_path = os.path.join(MODEL_SAVING_PATH, model_name)
    model.save(saving_path)

    model_infos = {
        "name": model_name,
        "VGG16_block_number": block_number,
        "neurone_number": neurone_number,
        "activation_function": activation_function,
        "accuracy": accuracy
    }

    json_model_infos = json.dumps(model_infos, indent = 4)

    with open(os.path.join(MODEL_SAVING_PATH, 'scores.csv'), 'a') as f:
        writer = csv.writer(f)
        writer.writerow([model_name, accuracy])

    with open(os.path.join(MODEL_SAVING_PATH, model_name, 'model_info.json'), 'w') as f:
        json.dump(json_model_infos, f)

    with open(os.path.join(MODEL_SAVING_PATH, model_name, 'model_info.pkl'), 'wb') as f:
        pickle.dump(model_infos, f)

    logging.info(f'model_name : {model_name}')
    logging.info(f'model_accuracy : {accuracy}')
    return f'Model {model_name} saved.'

if __name__ == "__main__":

    block_numbers = [1, 2, 3]
    neurones = [256, 512, 1024]
    activation_functions = ['relu', 'sigmoid', 'tanh']

    results = list()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for block_number in block_numbers:
            for neurone_number in neurones:
                for activation_function in activation_functions:
                    results.append(executor.submit(save_model_and_results, block_number, neurone_number, activation_function))

        for f in concurrent.futures.as_completed(results):
            print(f.result())


    # for block_number in range(3):
    #     for neurone_number in neurones:
    #         for activation_function in activation_functions:
    #             save_model_and_results(block_number + 1, neurone_number, activation_function)
