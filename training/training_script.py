import numpy as np
import os
import pickle

from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard

import logging

logging.basicConfig(level=logging.INFO)

PATH = '/home/ranto/code/RantoB/01.Projects/Image_Recognition/data-preparation/data'

def load_data(path):
    directory = os.listdir(path)

    data_path = input('File_name : ')

    if data_path == '':

        created_times = list()

        for file in directory:
            data_path = os.path.join(path, file)
            created_times.append(os.stat(data_path).st_ctime_ns)

        created_times = np.array(created_times)

        most_recent_file = directory[np.argmax(created_times)]

        logging.info(f'Most recent_file will be used : {most_recent_file}')

        data_path = os.path.join(path, most_recent_file)

    elif data_path not in directory:
        logging.info(f'no such fill : {data_path}')


    with open(data_path, "rb") as f:
        data = pickle.load(f)

def train():
    data = load_data(PATH)

    X_train, X_test, y_train, y_test = train_test_split(data['images'] / 255.,
                                                       data['y'],
                                                       test_size = .1,
                                                        stratify=data['y'])
    number_of_cat = len(np.unique(data['y']))

    y_train_cat = to_categorical(y_train, number_of_cat)
    y_test_cat = to_categorical(y_test, number_of_cat)

if __name__ == "__main__":
