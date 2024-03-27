# -*- coding: utf-8 -*-

from dash import Dash, dash_table
from dash.dependencies import Input, State, Output
from .DashAppNew import apply_layout_with_auth
from dash import dcc
from dash import html
from .templates.base import buildLayout 
from ..production.productionDataHandler import getFPYByDate, get_causes_by_PA
import plotly.express as px
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import dash_bootstrap_components as dbc

url_base = "/dash/failcauses/"

datepicker = dbc.CardHeader(
                className="Header-Disposition",
                children = [
                    dcc.DatePickerRange(
                        id="date-picker-range",
                        start_date_placeholder_text="Data início",
                        end_date_placeholder_text="Data fim",
                        display_format="DD/MM/YYYY",
                        minimum_nights=0
                    ),
                    dcc.Input(
                        id="idChoosenPA",
                        placeholder="Digite o PA",
                        type="text",
                        className="choosenPA",
                        maxLength=11,
                        style={"min-width":"50px", "max-width":"110px", "color":"#484848", "font-weight": "200", "font-size": "19px"}
                    ),
                    html.Button(
                        id="submit-button-state",
                        n_clicks=0,
                        children="Submit",
                        className = "btn btn-primary",
                        style={"margin-left":"5px"}
                    )
                ]
            )

def createLayout():
    graph = html.Div([
        html.Div([
            html.Div([
                datepicker,
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=html.Div([
                            dcc.Graph(id="output-graph",style={"min-width": "100px", "min-height":"50vh"})
                        ], id="loading-output-1")
                    ),
                ], className="card")
            ]),
            html.Div([
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-2",
                        type="default",
                        children=html.Div([
                            dash_table.DataTable(id="table_infos",
                                data = [],
                                editable=True,
                                filter_action="native",
                                sort_action="native",
                                sort_mode="multi",
                                row_selectable="multi",
                                row_deletable=True,
                                selected_rows=[],
                                page_action="native",
                                page_current= 0,
                                page_size= 10
                            )
                        ], id="loading-output-2")
                    ),
                ], className="card")
            ])
        ], className="plot")
    ])


    return graph

layout = buildLayout(body = createLayout())

def Add_Dash(server):
    app = Dash(server=server, url_base_pathname=url_base, assets_folder="./static/styles")
    apply_layout_with_auth(app, layout)

    # Define callback
    @app.callback(
    [Output("output-graph", "figure"),
     Output("date-picker-range", "start_date"),
     Output("date-picker-range", "end_date"),
     Output("date-picker-range", "min_date_allowed"),
     Output("date-picker-range", "max_date_allowed"),
     Output("table_infos", "columns"),
     Output("table_infos", "data")],
    [Input("submit-button-state", "n_clicks")],
    [State("date-picker-range", "start_date"),
     State("date-picker-range", "end_date"),
     State("idChoosenPA", "value")]
    )
    def update_graph(n_clicks,start_date,end_date,choosenPA):
        today = datetime.now().date()
        min_date = today - relativedelta(years=5)
        max_date = today - timedelta(days=1)

        print(choosenPA)

        if n_clicks != 0:

            df = ""
            df, dfTable = get_causes_by_PA(str(start_date).replace("-", ""), str(end_date).replace("-", ""), choosenPA)

            print(df)
            if df.empty:
                return {}, start_date, end_date, min_date, max_date, [], None
            else:
                figure = px.bar(df, x="STEP", y="Reprovações", title="Motivos", barmode="group", template="seaborn")
                figure.update_traces(marker_line_color = "black", marker_line_width = 1)

            print(dfTable)
            columns = [{"id": index, "name": column, "deletable": False} for index, column in enumerate(dfTable.columns)]

            return figure, start_date, end_date, min_date, max_date, columns, dfTable.values
        else:
            return {}, max_date, max_date, min_date, max_date, [], None

    return app.server