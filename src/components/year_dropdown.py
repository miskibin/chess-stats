from dash import Dash, html, dcc
import pandas as pd
from src.components import ids
from dash.dependencies import Input, Output

def get_years(df: pd.DataFrame) -> list:
    years = [v for v in df['date'].dt.year.unique()]
    labels = [{"label": y, "value": y} for y in years]
    return labels


def render(app: Dash, df: pd.DataFrame) -> html.Div:
    return html.Div(
        className='app-div',
        style={'margin': '10px'},
        children=[
            html.H6('year'),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                multi=True,
                options=get_years(df),
                value=[2020],
                style={'width': '20vw', 'color': 'black'}
            ),
            # html.Button(
            #     className='dropdown-button',
            #     children=['Select All'],
            #     id=ids.SELECT_ALL_YEARS_BUTTON
            # )
        ])
