from src.components import ids
from dash import Dash, html
from src.components import dropdown, scatter_chart, bar_chart, time_class_dropdown, section, year_dropdown


def create_layout(app: Dash, df) -> html.Div:
    return html.Div(
        className='app-div',
        style={'margin': '10px', 'display': 'flex', 'flexDirection': 'column',
               'alignItems': 'center', 'textAlign': 'center'},
        children=[
            section.create_section(
                children=[
                    year_dropdown.render(app, df),
                    dropdown.render(df, 'x label', id=ids.X_DROPDOWN),
                    dropdown.render(df, 'y label', id=ids.Y_DROPDOWN),
                    dropdown.render(df, 'group by', id=ids.GROUP_DROPDOWN, cols=[
                                    'player_elo', 'time_class'])],
                graph=scatter_chart.render(app, df), name='Scatter Chart'),
            html.Hr(),
            section.create_section(
                children=[
                    year_dropdown.render(app, df, id=ids.YEAR_DROPDOWN_BAR),
                    time_class_dropdown.render(app, df)],
                graph=bar_chart.render(app, df), name='Bar Chart')
        ])
