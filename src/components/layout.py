import sys
sys.path.append('')

from dash import Dash, html
from src.components import year_dropdown, bar_chart, x_dropdown, y_dropdown, group_dropdown

def create_layout(app: Dash, df) -> html.Div:
    return html.Div(
        className='app-div',
        style={'margin': '10px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center','textAlign': 'center'},
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className = 'dropdawn-container',
                style={'display': 'flex', 'flex-direction': 'row'},
                children=[
                    year_dropdown.render(app, df),
                    x_dropdown.render(app, df),
                    y_dropdown.render(app, df),
                    group_dropdown.render(app, df),
                ]
            ),
            bar_chart.render(app, df)
        ])