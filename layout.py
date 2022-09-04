from src.gui import ids
from dash import Dash, html
from src.components import dropdown, scatter_chart, bar_chart, time_class_dropdown, section, year_dropdown
import dash_bootstrap_components as dbc
import pandas as pd 

def get_df() -> pd.DataFrame:
    df =  pd.read_csv('data/games.csv')
    df['date'] = pd.to_datetime(df['date'])
    df.index = df['date']
    return df

def create_layout(app: Dash, df) -> html.Div:

    tab1 = dbc.Card(
        dbc.CardBody([
            section.create_section(
                children=[], name='Should I play now? . . .', graph=None),
            html.Hr()
        ]))
    tab2 = dbc.Card(
        dbc.CardBody([
            section.create_section(
                children=[
                    year_dropdown.render(app, df),
                    dropdown.render(df, 'x label', id=ids.X_DROPDOWN),
                    dropdown.render(df, 'y label', id=ids.Y_DROPDOWN),
                    dropdown.render(df, 'group by', id=ids.GROUP_DROPDOWN, cols=[
                                    'player_elo', 'time_class'])],
                graph=scatter_chart.render(app, df), name='Scatter Chart'),
            html.Hr()]))



    return dbc.Tabs(
        [
            dbc.Tab(tab1, label="Tab 1"),
            dbc.Tab(tab2, label="Tab 2"),
            dbc.Tab(tab3, label="Tab 3"),
        ]
    )
