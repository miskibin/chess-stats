from dash import Dash, html, dcc
import plotly.express as px
import ids
import pandas as pd
from dash.dependencies import Input, Output

def get_win_ratio_per_hour(df: pd.DataFrame, time_classes) -> pd.DataFrame:
    if type(time_classes) == str:
        time_classes = [time_classes]
    dff = pd.DataFrame(index=list(range(0,24)))
    for time_class in time_classes:
        dff2 = df.loc[df['time_class'] == time_class]
        total_games = dff2.groupby(dff2['date'].dt.hour).count()['result']
        won_games = dff2.groupby(dff2['date'].dt.hour).sum()['result']
        dff.insert(len(dff.columns), time_class+' win ratio', round(won_games/total_games,2)*100)
        dff.insert(len(dff.columns), 'total '+time_class+' games', total_games)
    return dff
    
def render(app: Dash, df: pd.DataFrame) -> html.Div:
    @app.callback(
    Output(ids.BAR_CHART, 'children'),
    [Input(ids.YEAR_DROPDOWN_BAR, 'value'), Input(ids.TIME_CLASS_DROPDOWN, 'value')])
    def update_bar_chart(years: list, time_class) -> html.Div:
        dff = df.query('date.dt.year in @years')
        fig = px.bar(get_win_ratio_per_hour(dff, time_class),barmode='group',text_auto=True)
        fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = list(range(0,24)),
            ticktext = list(range(0,24))
        ))
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART, style={'width': '95vw', 'height': '100%'})
    return html.Div(id=ids.BAR_CHART)