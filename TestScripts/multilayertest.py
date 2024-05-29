import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__)

# Sample data for the scattermapbox layer
data_scatter = [
    {'lat': 37.7749, 'lon': -122.4194, 'name': 'San Francisco'},
    {'lat': 34.0522, 'lon': -118.2437, 'name': 'Los Angeles'},
    {'lat': 40.7128, 'lon': -74.0060, 'name': 'New York City'},
]

# Create Scattermapbox trace
scatter_trace = go.Scattermapbox(
    lat=[city['lat'] for city in data_scatter],
    lon=[city['lon'] for city in data_scatter],
    mode='markers',
    marker=dict(size=12, color='rgb(0, 0, 255)'),
    text=[city['name'] for city in data_scatter],
    hoverinfo='text'
)

# Create Choropleth Mapbox figure using Plotly Express
choropleth_fig = px.choropleth_mapbox(
    locations=["CA", "TX", "NY"],
    color=[50, 70, 90],
    geojson='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json',
    mapbox_style="carto-positron",
    zoom=3,
    center={"lat": 37.0902, "lon": -95.7129},
    opacity=0.5
)

# Add Scattermapbox trace to Choropleth Mapbox figure
choropleth_fig.add_trace(scatter_trace)

app.layout = html.Div([
    dcc.Graph(
        id='map',
        figure=choropleth_fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
