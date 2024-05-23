import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

app = dash.Dash(__name__)

# PostgreSQL connection details
DATABASE_URL = 'postgresql+psycopg2://myuser:mypassword@localhost/mydatabase'

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Example function to query data
def get_data():
    query = "SELECT * FROM mytable"
    df = pd.read_sql(query, engine)
    return df

# Dash layout
app.layout = html.Div([
    html.H1('PostgreSQL and Dash Integration'),
    dcc.Graph(id='example-graph'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # in milliseconds
        n_intervals=0
    )
])

# Callback to update graph
@app.callback(
    Output('example-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    df = get_data()
    figure = {
        'data': [
            {'x': df['column1'], 'y': df['column2'], 'type': 'line', 'name': 'Data'}
        ],
        'layout': {
            'title': 'Data from PostgreSQL'
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
