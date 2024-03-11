from dash import html

def buildLayout(body):

    layout = html.Div([
        html.Section([
            html.Div([
                html.Nav([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.A("Inicio",href="/", className="navbar-item"),
                                html.A("Plot 1",href="/dash/app1", className="navbar-item"),
                                html.A("Plot 2",href="/dash/app2", className="navbar-item"),
                                html.A("Perfil",href="/profile", className="navbar-item"),
                                html.A("Sair",href="/logout", className="navbar-item")
                            ], className="navbar-end")
                        ], id = "navbarMenuHeroA", className="navbar-menu")
                    ], className="container")
                ], className="navbar")
            ], className="hero-head"),
            html.Div([
                body
            ])
        ], className="hero is-primary is-fullheight")
    ])

    return layout