import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


def create_map():
	# Sample data: replace with your actual data
	data = pd.DataFrame({
		'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
		'Latitude': [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
		'Longitude': [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740],
		'Population': [8419000, 3980400, 2716000, 2328000, 1690000]
	})

	# Create the map figure
	fig = px.scatter_mapbox(
		data, 
		lat="Latitude", 
		lon="Longitude", 
		hover_name="City", 
		hover_data=["Population"],
		color_discrete_sequence=["fuchsia"], 
		zoom=0, 
		height=500,
	)
	fig.update_layout(mapbox_style="open-street-map",margin=dict(l=0, r=0, t=0, b=0))


	# Define the layout
	layout = html.Div([
		dcc.Graph(id='map', figure=fig),
		dcc.Slider(
			id='zoom-slider',
			min=1,
			max=15,
			value=3,
			marks={i: str(i) for i in range(1, 16)},
			step=1
		)
	])

	# Define callback to update map zoom level
	@dash.callback(
		Output('map', 'figure'),
		[Input('zoom-slider', 'value')]
	)
	def update_map(zoom_level):
		fig.update_layout(mapbox=dict(zoom=zoom_level))
		return fig

	return layout
# # Run the app
# if __name__ == '__main__':
# 	app.run_server(debug=True)
