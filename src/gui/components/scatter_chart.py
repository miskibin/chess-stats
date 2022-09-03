from dash import Dash, html, dcc
import plotly.express as px
import ids
import pandas as pd
from dash.dependencies import Input, Output


def render(app: Dash, df: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.SCATTER_CHART, 'children'),
        [Input(ids.YEAR_DROPDOWN, 'value'), Input(ids.X_DROPDOWN, 'value'),
         Input(ids.Y_DROPDOWN, 'value'),Input(ids.GROUP_DROPDOWN, 'value')])
    def update_scatter_chart(years: list, x_label, y_label, group_label) -> html.Div:
        if type(years) != list:
            years = [years]
        dff = df.query('date.dt.year in @years')
        fig = px.scatter(dff, x=dff[x_label], y=dff[y_label], color=dff[group_label])
        return html.Div(dcc.Graph(figure=fig), id=ids.SCATTER_CHART, style={'width': '95vw', 'height': '100%'})
    return html.Div(id=ids.SCATTER_CHART)
