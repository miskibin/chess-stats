from dash import Dash, html
import dash_bootstrap_components as dbc
import pandas as pd 

def create_section(children:list, graph, name):
    return html.Section(
        children=[
            html.H1(name, style={'margin': '20px', 'text-align': 'center'}),
            html.Hr(),
            html.Div(
                className='dropdown-container',
                style={'display': 'flex', 'flex-direction': 'row', 'flex-shrink': '0', },
                children=children
            ),
            graph
        ],
        style={'width': '100%', 'height': '80vh'})
