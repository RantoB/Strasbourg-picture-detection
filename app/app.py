import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import cv2
from tensorflow.keras.models import load_model
from utils import *

app = dash.Dash()

model_2 = load_model('./Models/model_2')
model_3 = load_model('./Models/model_3')
with open('./data/data-64.pkl', 'rb') as f:
    data = pickle.load(f)
target_names = data['target_name_for_answer']

# app.scripts.config.serve_locally = True

details = list()

details.append(dcc.Markdown(children="Vous pouvez tester l'algorithme en postant une photo d'un de ces lieux. \
        La photo doit être prise du sol. Le batiment ou la statue doivent être vus de \
        face et doivent se trouver plus ou moins au centre de l'image."))

details.append(dcc.Markdown(children="N'hésitez pas à tester avec d'autres images pour voir si l'algorithme \
        remarque bien qu'il ne s'agit d'aucun des monuments qu'il connait."))

details.append(dcc.Markdown(children="Note: c'est un projet en cours de développement. La collecte de données \
        est en cours et le nombre de lieux identifiables va augmenter."))


infos = list()

infos.append(html.P(children=["- L'application est développée en Python.\
        L'image Docker de l'application est disponible sur Dockerhub: ",
        html.A(children="rantob/image_reco_stras", href="https://hub.docker.com/r/rantob/image_reco_stras"),
        ". L'application est déployée sur Cloud Run de Google Cloud Platform."]))

infos.append(html.H6("Autres projets:"))

infos.append(html.P(children=["- Dashboard de production d'électricité en France et modèle de prédiction de la demande d'électricité déployé en prototype sur Heroku: ",
        html.A(children="electricity demand model", href="https://electricityinfrance.herokuapp.com/")]))

infos.append(html.P(children=["- Jeux de piste géants au centre ville de Strasbourg: ",
        html.A(children="ENIGMA Strasbourg.", href="https://enigmastrasbourg.com"),
        " Ainsi que son chatbot développé avec RASA et déployé avec docker-compose \
        sur Google Compute Engine de Google Cloud Platform."]))

infos.append(html.P(children=["Développé par ", html.A(children="Bertrand BURCKER",
        href="https://www.linkedin.com/in/bertrand-burcker-a6192655/")]))

# info.append(html.Div([<div class="LI-profile-badge",
#   data-version="v1",
#    data-size="medium",
#     data-locale="fr_FR",
#      data-type="horizontal",
#       data-theme="light",
#        data-vanity="bertrand-burcker-a6192655"> <a class="LI-simple-link" ,
#                                         href='https://fr.linkedin.com/in/bertrand-burcker-a6192655?trk=profile-badge'> Bertrand Burcker</a>
#                                         </div>)

def consecutive_elements(elements: list)-> list:

    result = list()

    for element in elements:
        result.append(element)
        result.append(html.Br())

    return result

with open('./data/encoded_sample_images', 'rb') as f:
    encoded_sample_images = pickle.load(f)

app.layout = html.Div([
    html.Div([

        html.H3("Les monuments de Strasbourg"),
        html.Br(),

        dcc.Markdown(children="Ceci est un prototye de modèle de deep learning pour \
                la reconnaissance de monuments de Strasbourg."),
        html.Br(),

        dcc.Markdown(children="Pour l'instant, seuls les six lieux suivants sont identifiables:"),
        html.Br(),

        html.Div([ # Line with 3 first images
            html.Div([
                html.Img(src=f'data:image/jpeg;base64,{encoded_sample_images[0]}'),
                dcc.Markdown("Cathédrale Notre Dame de Strasbourg")

            ], className="four columns"),

            html.Div([
                html.Img(src=f'data:image/jpeg;base64,{encoded_sample_images[1]}'),
                dcc.Markdown("Lycée International des Pontonniers")
            ], className="four columns"),

            html.Div([
                html.Img(src=f'data:image/jpeg;base64,{encoded_sample_images[2]}'),
                dcc.Markdown("Eglise Saint Thomas")
            ], className="four columns"),
        ], className="row"),

        html.Div([ # Line with 3 next images
            html.Div([
                html.Img(src=f'data:image/jpeg;base64,{encoded_sample_images[3]}'),
                dcc.Markdown("Le palais Rohan")

            ], className="four columns"),

            html.Div([
                html.Img(src=f'data:image/jpeg;base64,{encoded_sample_images[4]}'),
                dcc.Markdown("L'opéra")
            ], className="four columns"),

            html.Div([
                html.Img(src=f'data:image/jpeg;base64,{encoded_sample_images[5]}'),
                dcc.Markdown("L'Aubette à la place Kléber")
            ], className="four columns"),
        ], className="row"),

        html.Div([ # Line with 2 col : some text and the POST image area
            html.Div([ # Text
                html.Div(consecutive_elements(details)),
            ], className="six columns",
            style={
                'text-align': 'left'
            }),

            html.Div([ # Image POST area
                dcc.Upload(
                    id='upload-image',
                    children=html.Div([
                        'Glissez votre fichier ou ',
                        html.A('parcourez vos dossiers.')
                    ]),
                    style={
                        'width': '100%',
                        'height': '120px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    multiple=False # Don't allow multiple files to be uploaded
                ),

                html.Div(id='output-image-upload'),
            ], className="six columns"),
        ], className="row"),

        html.Hr(),

        html.Div([
            html.Div([ # empty area on the left
                html.P('')
            ], className="six columns"),

            html.Div([ # Other projects...
                html.Div(consecutive_elements(infos)),
            ], className="six columns",
            style={
                'text-align': 'left'
            })

        ], className='row'),

    ], className="row"),
], style={
    'width': '75%',
    'margin-left':'12.5%',
    'margin-right':'12.5%'
         }
)

# app.scripts.append_script([{"external_url": "https://platform.linkedin.com/badges/js/profile.js",
#                             "async": True,
#                             "defer": True}])

def prediction(image_arr: np.ndarray) -> tuple:
    """
    This function takes as input the image posted by the user
    and processed by utils.convert_input_to_arr() fonction
    Returns the array of probabilities
    and the max probability value.
    -> (array_of_probabilities, max_proba_value)
    """
    # user picture processing
    image_arr = process_images_for_model(image_arr)
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

@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')])
def update_output(image):
    if not image:
        return

    # Convert input to numpy array
    image_arr = convert_input_to_arr(image)

    # Display the picture
    saving_path = './tested_pictures/image_cv2.jpeg'
    picture = display_picture(image_arr, saving_path)

    if picture == False:
        answer = "⚠️ Ce document n'a pas le format d'une image ⚠️"

        result = html.Div([
            html.P(answer)
        ])
        return result

    else:
        # prediction probabilities
        pred, proba_pred = prediction(image_arr)

        # Generate answer string to de displayed to the user
        answer = result_for_user(pred, proba_pred, target_names)

        result = html.Div([
            html.Img(src=f'data:image/jpeg;base64,{picture}'),
            html.P(answer)
        ])
        return result

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)
