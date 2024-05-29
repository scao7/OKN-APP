import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import time

app = dash.Dash(__name__)

# Layout for the first content
content_before_map = html.Div(id='content-before-map')

# Layout for the map content
map_layout = html.Div(id='map-content')

# Layout for the second content
content_after_map = html.Div(id='content-after-map')

# Callback to load content before the map
@app.callback(
    Output('content-before-map', 'children'),
    [],
    []
)
def load_content_before_map():
    # Simulate loading delay for content before map
    time.sleep(3)
    return html.Div([
        html.H3('Content Before Map Loaded'),
        html.P('This is content before the map.')
    ])

# Callback to load map content
@app.callback(
    Output('map-content', 'children'),
    [],
    []
)
def load_map_content():
    # Simulate loading delay for the map
    time.sleep(3)
    # Replace this with your actual map generation code
    return dcc.Graph(
        id='map-graph',
        figure={
            'data': [{
                'type': 'scattermapbox',
                'lat': [40, 38, 36],
                'lon': [-75, -80, -85],
                'mode': 'markers'
            }],
            'layout': {
                'mapbox': {
                    'style': 'open-street-map',
                    'center': {'lat': 38.7, 'lon': -75.1},
                    'zoom': 5
                }
            }
        }
    )
# App layout
app.layout = html.Div([
    content_before_map,
    map_layout,
    content_after_map
])

# Callback to load content after the map
@app.callback(
    Output('content-after-map', 'children'),
    [],
    []
)
def load_content_after_map():
    # Simulate loading delay for content after map
    time.sleep(3)
    return html.Div([
        html.H3('Content After Map Loaded'),
        html.P('This is content after the map.')
    ])



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
