from dash import Dash, html
import dash_bootstrap_components as dbc
from components.layout import create_layout
import pandas as pd

def get_df() -> pd.DataFrame:
    df =  pd.read_csv('data/games.csv')
    df['date'] = pd.to_datetime(df['date'])
    df.index = df['date']
    return df
def main() -> None:
    df = get_df()
    app = Dash(external_stylesheets=[dbc.themes.DARKLY])
    app.title = 'chess dashboard'
    app.layout = create_layout(app, df)
    app.run(debug=True)
if __name__ == "__main__":
    main()