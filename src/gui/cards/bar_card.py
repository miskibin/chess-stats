from src.gui import ids
from dash import Dash, html
from src.gui.components import dropdown, scatter_chart, bar_chart, time_class_dropdown, section, year_dropdown
import dash_bootstrap_components as dbc


def create_bar_card(app, df):
        return dbc.Card(
        dbc.CardBody([
            section.create_section(
                children=[
                    year_dropdown.render(app, df, id=ids.YEAR_DROPDOWN_BAR),
                    time_class_dropdown.render(app, df)],
                graph=bar_chart.render(app, df), name='Bar Chart'),
            html.Hr()]))