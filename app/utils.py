from base64 import decodebytes
import numpy as np
import cv2
import pickle
from base64 import b64encode
from tensorflow.keras.models import load_model

def convert_input_to_arr(uploaded_image):
    image_bytes = decodebytes(uploaded_image.split(',')[1].encode('ascii'))
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    return cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)

def process_images_for_model(image_arr):
    image_arr = cv2.resize(image_arr, (64, 64))
    return np.array([image_arr]) / 255.

def display_picture(image_arr):
    resized_images_arr = cv2.resize(image_arr, (224, int(224 * image_arr.shape[0] / image_arr.shape[1])))
    images_file_name = 'assets/image_cv2.jpeg'
    cv2.imwrite(images_file_name, resized_images_arr)
    encoded_image = b64encode(open(images_file_name, 'rb').read())
    return encoded_image.decode()

def result_for_user(pred, proba_pred, target_names):

    if proba_pred >= .85:
        return f'Cette photo montre {target_names[np.argmax(pred)]}'

    elif proba_pred < .85 and proba_pred >= .7:
        pred_sort = np.argsort(pred[0])[-2:]
        res = f'Je ne suis pas sûr de moi, je dirais qu\'il s\'agit de {target_names[pred_sort[1]]}, mais j\'hésite aussi avec {target_names[pred_sort[0]]}'
        return res

    else:
        return 'Je suis désolé.\nA priori je ne sais pas que quoi il s\'agit.\n Pourriez-vous m\'envoyer une autre photo ?'
