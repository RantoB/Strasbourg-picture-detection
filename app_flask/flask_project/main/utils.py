import numpy as np
import cv2
from PIL import Image
import pickle
from flask import current_app
import os
import secrets
from tensorflow.keras.models import load_model

infos_1 = [
    {
        'content': "Vous pouvez tester l'algorithme en postant une photo \
                    d'un de ces lieux. La photo doit être prise du sol. \
                    Le batiment ou la statue doivent être vus de \
                    face et doivent se trouver plus ou moins au centre \
                    de l'image."
    },
    {
        'content': "N'hésitez pas à tester avec d'autres images pour voir \
                    si l'algorithme remarque bien qu'il ne s'agit d'aucun \
                    des monuments qu'il connait."
    },
    {
        'content': "Note: c'est un projet en cours de développement. \
                    La collecte de données est en cours et le nombre \
                    de lieux identifiables va augmenter."
    },
]

infos_2 = [
    {
        'content':  "L'application est développée en Python avec le framework \
                    Flask. L'image Docker de l'pageslication est disponible sur \
                    Dockerhub: rantob/image_reco_stras. L'pageslication est \
                    déployée sur Cloud Run de Google Cloud Platform."
    },
    {
        'content': "Autres projets: "
    },
    {
        'content': "Dashboard de production d'électricité en France et modèle \
                    de prédiction de la demande d'électricité déployé en \
                    prototype sur Heroku: electricity demand model"
    },
    {
        'content': "Jeux de piste géants au centre ville de Strasbourg: \
                    ENIGMA Strasbourg. Ainsi que son chatbot développé avec \
                    RASA et déployé avec docker-compose sur Google Compute \
                    Engine de Google Cloud Platform."
    },
    {
        'content': "Développé par Bertrand BURCKER"
    },
]

pic_names ={
    "cathedrale": "Cathédrale Notre Dame de Strasbourg",
    "pontonniers": "Lycée International des Pontonniers",
    "st_thomas": "Eglise Saint Thomas",
    "palais_rohan": "Le palais Rohan",
    "opera": "L'opéra",
    "aubette": "L'Aubette à la place Kléber",
}

def prediction(image_path) -> tuple:
    """
    This function takes as input the image posted by the user
    and processed by utils.convert_input_to_arr() fonction
    Returns the array of probabilities
    and the max probability value.
    -> (array_of_probabilities, max_proba_value)
    """
    model_2 = load_model(os.path.join(current_app.root_path, 'static/Models/model_2'))
    model_3 = load_model(os.path.join(current_app.root_path, 'static/Models/model_3'))
    # openning with cv2 and preprocessing for models
    image_arr = cv2.imread(image_path)
    image_arr = cv2.resize(image_arr, (64, 64))
    image_arr = np.array([image_arr]) / 255.
    # model_2 prodictions
    pred_mod_2 = model_2.predict([image_arr])
    # model_3 prodictions
    pred_mod_3 = model_3.predict([image_arr])
    # Combination predictions of models 2 and 3
    pred_23 = (pred_mod_2 + pred_mod_3) / 2.
    # max probability
    # [0] is because proba_pred_23.shape is (1, 7)
    proba_pred_23 = pred_23[0][np.argmax(pred_23)]
    return pred_23, proba_pred_23

def result_for_user(picture_filename)-> str:
    """
    Description on going
    """

    with open(os.path.join(current_app.root_path, 'static/data/data-64.pkl'), 'rb') as f:
        data = pickle.load(f)
    target_names = data['target_name_for_answer']

    image_path = os.path.join(current_app.root_path, "static/tested_pics", picture_filename)

    pred, proba_pred = prediction(image_path)

    if proba_pred >= .85:
        return f'Cette photo montre {target_names[np.argmax(pred)]}'

    elif proba_pred < .85 and proba_pred >= .7:
        pred_sort = np.argsort(pred[0])[-2:]
        res = f'Je ne suis pas sûr de moi, je dirais qu\'il s\'agit de {target_names[pred_sort[1]]}, mais j\'hésite aussi avec {target_names[pred_sort[0]]}'
        return res

    else:
        return 'Je suis désolé.\nA priori je ne sais pas que quoi il s\'agit.\n Pourriez-vous m\'envoyer une autre photo ?'

def picture_examples():
    picture_list = os.listdir(os.path.join(current_app.root_path, 'static/example_pics'))
    picture_list.sort()

    picture_dict = dict()

    for picture in picture_list:
        for name_k, name_v in pic_names.items():
            if picture.find(name_k) > 0:
                picture_dict[picture] = name_v
    return picture_dict

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static',
                                'tested_pics', picture_filename)

    img = Image.open(form_picture)
    img_size = np.array(img).shape
    output_size = (224, int(224 * img_size[0] / img_size[1]))
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_filename
