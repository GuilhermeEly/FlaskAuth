from dash import Dash, ctx
from dash.dependencies import Input, Output, State
from .DashAppNew import apply_layout_with_auth
from dash import dcc
from dash import html
from .templates.base import buildLayout 
from ..production.productionDataHandler import getOverallFPY
import plotly.express as px
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd

url_base = "/dash/dashboard/"
minuteInterval = 60

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
                    html.Button(
                        id="submit-button-state2", 
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
                            html.Div([
                                dcc.Graph(id="output-graph", figure={}, style={"height":"70vh", "max-width":"100vh", "font-size": "54px"}),
                            ], style={"flex": "1"}, className="DivGraph"),
                            html.Div([
                                dcc.Graph(id="output-graph2", figure={}, style={"height":"70vh", "max-width":"100vh", "font-size": "54px"})
                            ], style={"flex": "1"}, className="DivGraph")
                        ], id="loading-output-1",style={"display": "flex", "height":"100%", "max-width":"100%"})
                    ),
                    dcc.Interval(
                        id="interval-component",
                        interval=(minuteInterval*60000), # in milliseconds
                        n_intervals=0
                    )
                ], className="card", style={"height":"100%", "width":"100%"})
            ])
        ])
    ])

    return graph



def Add_Dash(server):
    
    app = Dash(server=server, url_base_pathname=url_base, assets_folder="./static/styles")

    @app.callback(
    [Output("output-graph", "figure"),
     Output("output-graph2", "figure"),
     Output("date-picker-range", "start_date"),
     Output("date-picker-range", "end_date")],
    [Input("interval-component", "n_intervals"),
     Input("submit-button-state2", "n_clicks")],
    [State("date-picker-range", "start_date"),
     State("date-picker-range", "end_date")]
    )
    def update_graph_live(n, n_button, start_date, end_date):
        triggered_id = ctx.triggered_id
        if triggered_id != "submit-button-state2":
            today = datetime.now().date()
            first = today.replace(day=1)
            last_month_end = first - timedelta(days=1)
            last_month_begin = last_month_end.replace(day=1)
        else:
            last_month_begin = start_date
            last_month_end = end_date

        daysToFetch = pd.DataFrame(columns=["DIA", "TIPO", "FPY"])

        for i in range(10):
            day = datetime.now().date() - timedelta(1) - timedelta(i)

            day = str(day).split(" ")[0]
            fpyDay = getOverallFPY(str(day).replace("-", ""), str(day).replace("-", ""))

            df2 = pd.DataFrame([[day,"APROVADO",(fpyDay)]], columns=["DIA","TIPO", "FPY"])
            daysToFetch = pd.concat([df2, daysToFetch], ignore_index=True)
            df2 = pd.DataFrame([[day,"REPROVADO",(100-fpyDay)]], columns=["DIA","TIPO", "FPY"])
            daysToFetch = pd.concat([df2, daysToFetch], ignore_index=True)

        try:
            daysToFetch = daysToFetch.sort_values(by=["DIA","FPY","TIPO"], ascending=False)
            daysToFetch = daysToFetch.sort_values(by=["TIPO"], ascending=True)

            figure = px.bar(daysToFetch, x="DIA", y="FPY", color="TIPO", title="First Pass Yield (Últimos 10 dias)", template="seaborn")
            figure.update_layout(
                font=dict(
                    family="Aharoni",
                    size=27,
                )
            )
        except:
            figure = {}

        try:
            fpyold = getOverallFPY(str(last_month_begin).replace("-", ""), str(last_month_end).replace("-", ""))

            if type(last_month_end) is type(datetime.now().date()):
                print_last_month_end = last_month_end.strftime("%d/%m/%y")
                print_last_month_begin = last_month_begin.strftime("%d/%m/%y")

            else:
                print_last_month_end = datetime.strptime(last_month_end, "%Y-%m-%d").strftime("%d/%m/%y")
                print_last_month_begin = datetime.strptime(last_month_begin, "%Y-%m-%d").strftime("%d/%m/%y")

            titulo = "First Pass Yield de " +print_last_month_begin+ " à "+ print_last_month_end

            dold = {"TIPO": ["APROVADO", "REPROVADO"], "FPY": [fpyold, 100-(fpyold)]}
            dfold = pd.DataFrame(data=dold)
            figureold = px.pie(dfold, values="FPY", names="TIPO", hole=.3, title=titulo, template="seaborn")
            figureold.update_layout(
                font=dict(
                    family="Aharoni",
                    size=27,
                )
            )
        except:
            figureold = {}

        return figure, figureold, last_month_begin, last_month_end

    layout = buildLayout(body = createLayout())
    apply_layout_with_auth(app, layout)

    return app.server