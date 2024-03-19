from dash import Dash
from dash.dependencies import Input, Output
from .DashAppNew import apply_layout_with_auth
from dash import dcc
from dash import html
from .templates.base import buildLayout 
from ..production.productionDataHandler import getFPYByDate, getOverallFPY, getNewOverallFPY
import plotly.express as px
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd

url_base = "/dash/dashboard/"

def createLayout():
    graph = html.Div([
        html.Div([
            html.Div([
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=html.Div([
                            html.Div([
                                dcc.Graph(id="output-graph",figure={}),
                            ], style={"width": "50vh"}),
                            html.Div([
                                dcc.Graph(id="output-graph2",figure={})
                            ], style={"flex-grow": "1"})
                        ], id="loading-output-1",style={"display": "flex"})
                    ),
                    dcc.Interval(
                        id='interval-component',
                        interval=(600*1000), # in milliseconds
                        n_intervals=0
                    )
                ], className="card")
            ])
        ])
    ])

    return graph



def Add_Dash(server):
    
    app = Dash(server=server, url_base_pathname=url_base, assets_folder="./static/styles")

    @app.callback(
    [Output('output-graph', 'figure'),
     Output('output-graph2', 'figure')],
    [Input('interval-component', 'n_intervals')]
    )
    def update_graph_live(n):
        today = datetime.now().date()
        first = today.replace(day=1)
        last_month_end = first - timedelta(days=1)
        last_month_begin = last_month_end.replace(day=1)

        try:
            fpynew = getNewOverallFPY(str(last_month_begin).replace("-", ""), str(last_month_end).replace("-", ""))
            d = {'names': ["Approved", "Reproved"], 'values': [fpynew, 1-fpynew]}
            df = pd.DataFrame(data=d)
            figure = px.pie(df, values="values", names="names", hole=.3)
        except:
            figure = {}

        try:
            fpyold = getOverallFPY(str(last_month_begin).replace("-", ""), str(last_month_end).replace("-", ""))
            dold = {'names': ["Approved", "Reproved"], 'values': [fpyold, 100-(fpyold)]}
            dfold = pd.DataFrame(data=dold)
            figureold = px.pie(dfold, values="values", names="names", hole=.3)
        except:
            figureold = {}

        return figure, figureold

    layout = buildLayout(body = createLayout())
    apply_layout_with_auth(app, layout)

    return app.server