from dash import Dash, html, dcc
import pandas as pd
import ids
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

def get_years(df: pd.DataFrame) -> list:
    print(df['date'].dtype)
    return [int(v) for v in df['date'].dt.year.unique()]


def render(app: Dash, df: pd.DataFrame, id = ids.YEAR_DROPDOWN) -> html.Div:
    return html.Div(
        className='app-div',
        style={'margin': '10px'},
        children=[
            html.H4('year'),
            dcc.Dropdown(
                id=id,
                multi=True,
                clearable=False,
                options=get_years(df),
                value=[get_years(df)[0]],
                style={'width': '20vw', 'color': 'black', 'flex-grow': '0'}
            )
        ])
