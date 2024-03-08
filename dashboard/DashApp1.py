# -*- coding: utf-8 -*-

from dash import Dash
from dash.dependencies import Input, State, Output
from .DashAppNew import apply_layout_with_auth
import dash_core_components as dcc
import dash_html_components as html
from .templates.base import buildLayout 

url_base = '/dash/app1/'

graph = html.Div([
    html.Div([
        html.Div('This is dash app1', style={"width": "50%"}),
        dcc.Input(id = 'input_text', className="input", style={"margin-left": "50%"}),
        html.Div(id = 'target')
    ], style={"width": "100%"})
])

layout = buildLayout(body = graph)

def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base, assets_folder="./static/styles")
    apply_layout_with_auth(app, layout)

    @app.callback(
            Output('target', 'children'),
            [Input('input_text', 'value')])
    def callback_fun(value):
        return 'your input is {}'.format(value)
    
    return app.server