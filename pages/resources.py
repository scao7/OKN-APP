from dash import html
from dash import dcc
from dash.dependencies import Input, Output
# from app import app

layout = html.Div([
    html.H1('Resource Page'),
    dcc.Link('Go to About Page', href='/about')
])