import cv2
import os
import numpy as np
import pickle
from datetime import datetime as dt
import logging

logging.basicConfig(level=logging.INFO)

EXTENSION_LIST = ['.JPG', '.JPEG', '.PNG']

def get_all_path(path):
    sub_path_list = list()
    directories = os.listdir(path)
    for element in directories:
        sub_path = os.path.join(path, element)
        if os.path.isdir(sub_path):
            sub_path_list.append(sub_path)

    if sub_path_list:
        result = list(sub_path_list)
        for sub_path in sub_path_list:
            result.extend(list(get_all_path(sub_path)))
        return result
    else:
        return [path]

def build_data():

    path = "/media/ranto/AB0C-7457/3. ENIGMA Strasbourg - jeux et paperasse/5.Reconnaissance-d-images/images"

    directories = os.listdir(path)
    directories.sort()

    target_name_for_answer = dict()
    target_names = dict()
    images = list()
    y = list()

    for i, sub_dir in enumerate(directories):

        target_names[i] = sub_dir

        if 'cathedrale' in sub_dir.lower():
            target_name_for_answer[i] = 'la Cathédrale de Strasbourg.'
        elif 'pontonniers' in sub_dir.lower():
            target_name_for_answer[i] = 'le Lycée International des Pontonniers.'
        elif 'thomas' in sub_dir.lower():
            target_name_for_answer[i] = 'l\'église St Thomas.'
        elif 'rohan' in sub_dir.lower() and 'ill' in sub_dir.lower():
            target_name_for_answer[i] = 'le Palais Rohan depuis le quai des bateliers.'
        elif 'rohan' in sub_dir.lower() and 'chateau' in sub_dir.lower():
            target_name_for_answer[i] = 'le Palais Rohan depuis la place du château.'
        elif 'opéra' in sub_dir.lower():
            target_name_for_answer[i] = 'l\'opéra à la place Broglie'
        elif 'aubette' in sub_dir.lower():
            target_name_for_answer[i] = 'l\'Aubette à la place Kléber'
        elif 'ghandi' in sub_dir.lower():
            target_name_for_answer[i] = 'la statue de Ghandi'
        elif 'bourse' in sub_dir.lower():
            target_name_for_answer[i] = 'la salle des fêtes de la Bourse'
        elif 'administratif' in sub_dir.lower():
            target_name_for_answer[i] = 'le centre administratif de Strasbourg'
        elif 'danseuse' in sub_dir.lower():
            target_name_for_answer[i] = 'la statue de la danseuse'
        elif 'desaix' in sub_dir.lower():
            target_name_for_answer[i] = 'le monument Desaix'
        elif 'conservatoire' in sub_dir.lower():
            target_name_for_answer[i] = 'le conservatoire régional de Strasbourg'

        sub_path = os.path.join(path, sub_dir)
        all_sub_path = get_all_path(sub_path)

        for each_path in all_sub_path:
            for image_name in os.listdir(each_path):
                is_image_file = False
                for ext in EXTENSION_LIST:
                    is_image_file = is_image_file or image_name.endswith(ext.lower())
                if is_image_file:
                    image_path = os.path.join(each_path, image_name)
                    image = cv2.imread(image_path)
                    resized_image = cv2.resize(image, (64, 64))
                    images.append(resized_image)
                    y.append(i)

        logging.info(f'picture in "{sub_dir}" treated.')

    y = np.array(y)

    data = dict()
    data['images'] = np.array(images)
    data['target_names'] = target_names
    data['target_name_for_answer'] = target_name_for_answer
    data['y'] = y

    return data

def save_data():
    data = build_data()
    path = '/home/ranto/code/RantoB/01.Projects/Image_Recognition/data-preparation/data'

    time_stamp = dt.now()
    time_string = time_stamp.strftime('%H%M%d%m%Y')
    file_name = 'data' + time_string + '.pkl'
    saving_path = os.path.join(path, file_name)

    with open(os.path.join(saving_path), 'wb') as f:
        pickle.dump(data, f)

    logging.info(f'{file_name} saved.')

if __name__ == "__main__":
    """
    """
    save_data()
