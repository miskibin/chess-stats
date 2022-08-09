from dash import Dash, html, dcc
import pandas as pd

def get_labels(df:pd.DataFrame, cols):
    if cols:
        return [c for c in df.columns if c in cols]
    return [c for c in df.columns ]
    

def render(df: pd.DataFrame, name:str, id:str, cols = None) -> html.Div:
    return html.Div(
        style={'margin': '10px'},
        className='app-div',
        children=[
            html.H4(name),
            dcc.Dropdown(
                id=id,
                multi=False,
                value=get_labels(df, cols)[0],
                clearable=False,
                options=get_labels(df, cols),
                style={'width': '20vw', 'color': 'black'}
            ),
        ])
