from dash import html
import dash_bootstrap_components as dbc

def buildLayout(body):
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink("Dashboard", href="/dash/dashboard", external_link=True)
            ),
            dbc.NavItem(
                dbc.NavLink("Fpy", href="/dash/fpy", external_link=True)
            ),
            dbc.NavItem(
                dbc.NavLink("Causas", href="/dash/failcauses", external_link=True)
            ),
            dbc.NavItem(
                dbc.NavLink("Perfil", href="/profile", external_link=True)
            ),
            dbc.NavItem(
                dbc.NavLink("Sair", href="/logout", external_link=True)
            ),
        ],
        brand="First Pass Yield",
        brand_href="",
        color="primary",
        dark=True,
        brand_external_link=True,
        links_left=False
    )

    layout = html.Div([
        html.Div([
            navbar
        ]),
        dbc.CardBody([
            body
        ])
    ])

    return layout