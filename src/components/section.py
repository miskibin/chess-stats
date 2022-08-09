from dash import Dash, html

def create_section(children:list, graph, name):
    return html.Section(
        children=[
            html.H1(name, style={'margin': '20px'}),
            html.Hr(),
            html.Div(
                className='dropdown-container',
                style={'display': 'flex', 'flex-direction': 'row'},
                children=children
            ),
            graph
        ],
        style={'width': '100%', 'height': '100vh'})
