# -*- coding: utf-8 -*-

from dash import Dash
from dash.dependencies import Input, State, Output
from .DashAppNew import apply_layout_with_auth
from dash import dcc
from dash import html
from .templates.base import buildLayout 
from ..production.productionDataHandler import getFPYByDate
import plotly.express as px
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

url_base = '/dash/app2/'

def createLayout():
    graph = html.Div([
        html.Div(
            className='Header-Disposition',
            children =
            [
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date_placeholder_text='Data início',
                    end_date_placeholder_text='Data fim',
                    display_format='DD/MM/YYYY',
                    minimum_nights=0
                ),
                html.Button(
                    id='submit-button-state', 
                    n_clicks=0, 
                    children='Submit',
                    className = 'Submit-Button'
                )    
            ]
        ),
        html.Div([
            html.Div([
                dcc.Loading(
                    id="loading-1",
                    type="default",
                    children=html.Div([
                        dcc.Graph(id='output-graph')
                    ], id="loading-output-1")
                ),
            ], className="card")
        ], className="plot")
    ])

    return graph

layout = buildLayout(body = createLayout())

def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base, assets_folder="./static/styles")
    apply_layout_with_auth(app, layout)

    # Define callback
    @app.callback(
    [Output('output-graph', 'figure'),
     Output('date-picker-range', 'start_date'),
     Output('date-picker-range', 'end_date'),
     Output('date-picker-range', 'min_date_allowed'),
     Output('date-picker-range', 'max_date_allowed')],
    [Input('submit-button-state', 'n_clicks')],
    [State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date')]
    )
    def update_graph(n_clicks,start_date,end_date):
        today = datetime.now().date()
        min_date = today - relativedelta(years=5)
        max_date = today - timedelta(days=1)

        if n_clicks == 0:
            weekday = datetime.today().weekday()

            if weekday == 0:
                start_date = str((datetime.now() - timedelta(3))).split(" ")[0]
                end_date = str((datetime.now() - timedelta(3))).split(" ")[0]
            else:
                start_date = str((datetime.now() - timedelta(1))).split(" ")[0]
                end_date = str((datetime.now() - timedelta(1))).split(" ")[0]
        
        df = getFPYByDate(str(start_date).replace('-', ''), str(end_date).replace('-', ''))
        if df.empty:
            return {}, start_date, end_date, min_date, max_date
        else:
            figure = px.bar(df, x="PA", y="FPY", color="TIPO", title="First Pass Yield", barmode="group", template="seaborn", hover_data=["NOME", "PA"])
            figure.update_traces(marker_line_color = 'black', marker_line_width = 1)

        return figure, start_date, end_date, min_date, max_date

    return app.server