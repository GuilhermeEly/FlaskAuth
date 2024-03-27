# -*- coding: utf-8 -*-

from flask_login import current_user
from dash import html
import uuid

def apply_layout_with_auth(app, layout):
    def serve_layout():
        if current_user and current_user.is_authenticated:
            session_id = str(uuid.uuid4())
            return html.Div([
                html.Div(session_id, id="session_id", style={"display": "none"}),
                layout
            ])
        return html.Div("403 Access Denied")
    
    app.config.suppress_callback_exceptions = True
    app.layout = serve_layout