# -*- coding: utf-8 -*-

from dash import Dash
from dash.dependencies import Input, State, Output
from .DashAppNew import apply_layout_with_auth
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from .templates.base import buildLayout 

url_base = '/dash/app2/'

graph = html.Div([
    dcc.Input(
        id='input-number',
        type='number',
        value=10
    ),
    html.Div([
        dcc.Graph(id='output-graph')
    ], className="card")
])

layout = buildLayout(body = graph)

def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base, assets_folder="./static/styles")
    apply_layout_with_auth(app, layout)

    # Define callback
    @app.callback(
    Output('output-graph', 'figure'),
    [Input('input-number', 'value')]
    )
    def update_graph(input_number):
        x = np.linspace(0, 10, input_number)
        y = np.sin(x)
    
        figure = {
            'data': [{
                'x': x,
                'y': y,
                'type': 'scatter',
                'mode': 'lines',
                'name': 'sin(x)'
            }],
            'layout': {
                'title': 'Sin Function',
                'xaxis': {'title': 'X'},
                'yaxis': {'title': 'Y'}
            }
        }
    
        return figure

    return app.server