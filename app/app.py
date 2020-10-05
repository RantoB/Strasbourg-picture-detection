import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
# import numpy as np
# import pandas as pd
# import pickle
# import os

from utils import *

'''Instanciate app'''
app = dash.Dash(__name__)

server = app.server

app.title = 'Monuments Strasbourg'

# Messages
dashboard_name = 'Les monuments de Strasbourg'

description_tab_1 = 'Tab 1.'

description_tab_2 = 'Tab 2.'

description_tab_3 = 'Tab 3.'

description_tab_4 = 'Tab 4'

directory_path = '../'

app.layout = html.Div([
    html.H4(children=dashboard_name),

    dcc.Tabs([
        dcc.Tab(label='Label for tab 1', children=[
            html.H5(children=description_tab_1),

            html.Hr(),

            html.Div([ #
                html.Div([ # left columns radio items
                    html.Div(children=[
                        html.P('selector_1'),
                        dcc.RadioItems(
                            id='id_for_selector_1',
                            options=[
                                {'label': 'label 1', 'value': '1'},
                                {'label': 'label 2', 'value': '2'},
                                {'label': 'label 2', 'value': '3'},
                                {'label': 'label 3', 'value': '4'},
                                {'label': 'label 5', 'value': '5'}
                            ],
                            value='1',
                            labelStyle={"display": "block"}
                        ),
                    ], style={
                        'textAlign': 'left'},
                        className='radio_item'),

                    html.Div(children=[
                        html.P('selector_2'),
                        dcc.RadioItems(
                            id='id_for_selector_2',
                            options=[
                                {'label': 'label 1', 'value': '1'},
                                {'label': 'label 2', 'value': '2'},
                                {'label': 'label 2', 'value': '3'},
                                {'label': 'label 3', 'value': '4'},
                                {'label': 'label 5', 'value': '5'}
                            ],
                            value='1',
                            labelStyle={"display": "block"}
                        ),
                    ], style={
                        'textAlign': 'left'},
                    className='radio_item'),

                ], className="two columns"),

                html.Div([ # right column - top


                    dcc.Upload(
                        id='upload-image',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select a picture')
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

                    html.Div(id='output_callback_1', className="row")
                ], className="ten columns"),

                html.Div([ # right column - bottom
                    html.Div(id='output_callback_2', className="row")
                ], className="ten columns")

            ], className="row")],
            className='custom-tab',
            selected_className='custom-tab--selected'),

        dcc.Tab(label='Label for tab 2', children=[
            html.H5(children=description_tab_2),
                html.Hr(),

                html.Div([ #
                    html.Div([ # left columns radio items
                        html.Div(children=[
                            html.P('Selector 3'),
                            dcc.RadioItems(
                                id='id_for_selector_3',
                                options=[
                                    {'label': 'label 1', 'value': '1'},
                                    {'label': 'label 2', 'value': '2'},
                                    {'label': 'label 2', 'value': '3'},
                                    {'label': 'label 3', 'value': '4'},
                                    {'label': 'label 5', 'value': '5'}
                                ],
                                value='1',
                                labelStyle={"display": "block"}
                            ),
                        ], style={
                            'textAlign': 'left'},
                            className='radio_item'),

                        html.Div(children=[
                            html.P('Selector 4'),
                            dcc.RadioItems(
                                id='id_for_selector_4',
                                options=[
                                    {'label': 'label 1', 'value': '1'},
                                    {'label': 'label 2', 'value': '2'},
                                    {'label': 'label 2', 'value': '3'},
                                    {'label': 'label 3', 'value': '4'},
                                    {'label': 'label 5', 'value': '5'}
                                ],
                                value='1',
                                labelStyle={"display": "block"}
                            ),
                        ], style={
                            'textAlign': 'left'},
                        className='radio_item'),

                    ], className="two columns"),

                    html.Div([ # right column - top : map and barplot
                        html.Div(id='output_callback_3', className="row")
                    ], className="ten columns"),

                    html.Div([ # right column - bottom : line graph
                        html.Div(id='output_callback_4', className="row")
                    ], className="ten columns")

                ], className="row")
            ],
            className='custom-tab',
            selected_className='custom-tab--selected'),

        dcc.Tab(label='Label for tab 3', children=[
            html.H5(children=description_tab_3),
            html.Hr(),
            html.Div([ # Main Div
                html.Div([ # SARIMAX Div
                    html.Div([ # Left column Div
                        html.P("text here"),
                        dcc.Input(
                            id="input_1", type="number",
                            value=7, min=1, max=30),

                        html.P("text again here"),
                        dcc.Input(
                            id="input_2", type="number",
                            value=2, min=1, max=14),
                    ], className="two columns"), # Left column Div

                    html.Div([ # Right column Div
                        html.H6("blablabla."),
                        html.Div(id='output_callback_5', className='row'),

                        html.Br(),

                        html.Div([
                            html.H6("blablabla."),
                        ], className='row')
                    ], className="ten columns") # Right column Div
                ]), # SARIMAX Div

                html.Div([ # PROPHET Div
                    html.Div([ # Left column Div
                        html.Hr(),
                        html.P("youhou !!"),
                        dcc.Input(
                            id="input_3", type="number",
                            value=24, min=1, max=168)
                    ], className="two columns"), # Left column Div

                    html.Div([ # Right column Div
                        html.Hr(),
                        html.H6("one more !"),
                        html.Div([
                            # Reality and model comparison
                            html.Div(id='output_callback_6', className='row'),
                        ], className='row')
                    ], className="ten columns") # Right column Div
                ]) # PROPHET Div
            ]) # Main Div
        ],
            className='custom-tab',
            selected_className='custom-tab--selected'),

        dcc.Tab(label='Label for tab 4', children=[
                    html.H5(children=description_tab_4),

                    html.Hr(),

                    html.Div([ #
                        html.Div([ # left columns

                        ], className="two columns"),

                        html.Div([ # right column
                            html.P('text 1'),
                            html.A('link'),
                            html.Hr(),

                            html.P('text 2'),
                            html.A('link'),
                            html.Hr(),

                            html.P('text 3'),
                            html.A('link'),
                            html.Hr(),

                            html.P('text 4'),
                            html.A('link'),
                            html.Hr(),

                            html.P('text 5'),
                            html.A('link'),

                        ], className="ten columns")
                    ], className="row")
                ],
             className='custom-tab',
             selected_className='custom-tab--selected'),

    ], className='custom-tabs')
])

@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')])
def update_output(image):
    if not image:
        return html.P('this is not a picture')
    else:
        return html.Img(src=image)

# Callback for Tab 1
@app.callback(
    dash.dependencies.Output('output_callback_1', 'children'),
    [dash.dependencies.Input('id_for_selector_1', 'value'),
    dash.dependencies.Input('id_for_selector_2', 'value')])
def callback_1(id_for_selector_1, id_for_selector_2):
    result = f'{id_for_selector_1} and {id_for_selector_2} have been selected.'
    return result

@app.callback(
    dash.dependencies.Output('output_callback_2', 'children'),
    [dash.dependencies.Input('id_for_selector_2', 'value')])
def callback_2(id_for_selector_2):
    result = f'{id_for_selector_2} have been selected.'
    return result

# Callback for Tab 2
@app.callback(
    dash.dependencies.Output('output_callback_3', 'children'),
    [dash.dependencies.Input('id_for_selector_3', 'value'),
    dash.dependencies.Input('id_for_selector_4', 'value')])
def callback_3(id_for_selector_3, id_for_selector_4):
    result = f'{id_for_selector_3} and {id_for_selector_4} have been selected.'
    return result

@app.callback(
    dash.dependencies.Output('output_callback_4', 'children'),
    [dash.dependencies.Input('id_for_selector_4', 'value')])
def callback_4(id_for_selector_4):
    result = f'{id_for_selector_4} have been selected.'
    return result

# Callback for Tab 3
@app.callback(
    Output("output_callback_5", "children"),
    [Input("input_1", "value"),
    Input("input_2", "value")],
)
def callback_5(input_1, input_2):
    return f'inputs are: {input_1} and {input_2}'

@app.callback(
    Output("output_callback_6", "children"),
    [Input("input_3", "value")],
)
def callback_6(input_3):
    return f'input is: {input_3}'

def parse_contents(images, images_name):

    try:
        if images_name.endswith('.jpeg'):
            pass

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(images_name),

        html.Hr(),  # horizontal line

    ])

if __name__ == '__main__':
    app.run_server(debug=True)
