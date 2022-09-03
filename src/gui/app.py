from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc
from layout import create_layout
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = 'chess dashboard'
app.layout = create_layout(app, None) 
if __name__ == '__main__':
    app.run_server(debug=True)
