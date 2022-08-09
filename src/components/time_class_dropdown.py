from dash import Dash, html, dcc
import pandas as pd
from src.components import ids
from dash.dependencies import Input, Output

def get_years(df: pd.DataFrame) -> list:
    labels = [v for v in df['time_class'].unique()]
    return labels


def render(app: Dash, df: pd.DataFrame, id = ids.TIME_CLASS_DROPDOWN) -> html.Div:
    return html.Div(
        className='app-div',
        style={'margin': '10px'},
        children=[
            html.H4('time class'),
            dcc.Dropdown(
                id=id,
                multi=True,
                options=get_years(df),
                value='rapid',
                clearable=False,
                style={'width': '20vw', 'color': 'black'}
            )
        ])
