import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
# from base64 import b64encode
import cv2
#import dash_table_experiments as dt

# import datetime
# import json
# import pandas as pd
# import plotly
# import io
# import numpy as np
# from base64 import decodestring

from utils import *

from tensorflow.keras.models import load_model

app = dash.Dash()

model_2 = load_model('Models/model_2')
model_3 = load_model('Models/model_3')
with open('../data/data-64.pkl', 'rb') as f:
    data = pickle.load(f)
target_names = data['target_name_for_answer']

# app.scripts.config.serve_locally = True

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-image-upload'),
])

def prediction(image_arr):
    image_arr = process_images_for_model(image_arr)

    pred_mod_2 = model_2.predict([image_arr])
    pred_mod_3 = model_3.predict([image_arr])
    pred_23 = (pred_mod_2 + pred_mod_3) / 2.

    proba_pred_23 = pred_23[0][np.argmax(pred_23)]

    return pred_23, proba_pred_23


@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')])
def update_output(image):
    if not image:
        return

    image_arr = convert_input_to_arr(image)

    picture = display_picture(image_arr) # To display the picture

    # Code for model prediction
    pred, proba_pred = prediction(image_arr)

    # prediction = target_names[np.argmax(model.predict(image_arr))]

    answer = result_for_user(pred, proba_pred, target_names)

    result = html.Div([

        # html.Img(src=app.get_asset_url('image_cv2.jpeg')),
        html.Img(src=f'data:image/jpeg;base64,{picture}'),
        # html.Img(src=image),
        html.P(answer)
    ])

    return result

if __name__ == '__main__':
    app.run_server(debug=False)
