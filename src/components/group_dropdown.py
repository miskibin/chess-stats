from dash import Dash, html, dcc
import pandas as pd
from src.components import ids
from dash.dependencies import Input, Output

def get_labels(df:pd.DataFrame):
    columns = [c for c in df.columns]
    labels = []
    for column in columns:
        labels.append({"label": column, "value": column})
    return labels


def render(app: Dash, df: pd.DataFrame) -> html.Div:
    return html.Div(
        style={'margin': '10px'},
        className='app-div',
        children=[
            html.H6('group'),
            dcc.Dropdown(
                id=ids.GROUP_DROPDOWN,
                multi=False,
                value='time_class',
                options=get_labels(df),
                style={'width': '20vw', 'color': 'black'}
            ),
        ])
