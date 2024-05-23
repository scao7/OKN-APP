import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json
from urllib.request import urlopen

from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine, text, Column, Integer, String, Sequence
import os 

def create_map():
	# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
	# 	counties = json.load(response)
	# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
	# 				dtype={"fips": str})
	
	counties = json.load(open(r"Datasets\geojson-counties-fips.json",'r'))
	# df = pd.read_excel(r"Datasets\ruralurbancodes2013.xls",dtype={"FIPS": str})

	# create using database conneciton 
	password = os.environ["okn_database"]
	engine = create_engine(f'postgresql+psycopg2://postgres:{password}@127.0.0.1:5432/dummy')
	df = pd.read_sql("SELECT rural_urban.rural_urban_code, rural_urban.rucc FROM public.rural_urban ORDER BY rural_urban_id ASC", engine)
	# Try to connect and execute a simple query
	try:
		# Connect to the database
		with engine.connect() as connection:
			# Execute a test query
			result = connection.execute(text("SELECT version();"))
			# Fetch the result
			version = result.fetchone()
			print(f"Database connection successful. PostgreSQL version: {version[0]}")
	except Exception as e:
		print(f"An error occurred: {e}")


	# Create a choropleth mapbox
	fig = px.choropleth_mapbox(df, geojson=counties, locations='rural_urban_code', color='rucc',
							color_continuous_scale="Viridis",
							range_color=(1, 9),
							mapbox_style="open-street-map",
							zoom=7, center = {"lat": 33.2098, "lon": -87.5692}, 
							opacity=0.5,
							labels={'RUCC_2013':'RUCC_2013'},
							)
	fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
				   coloraxis_colorbar=dict(
						x=0,
						y=1,  # Adjust the position of the color bar to be on top
						yanchor='top',  # Anchor the color bar to the top of the map
						xanchor='left',  # Anchor the color bar to the left side
						thickness=20  # Set the thickness of the color bar
    				)
	)
	

	# Define the layout
	layout = html.Div([
		dcc.Graph(id='map', figure=fig),
		# dcc.Slider(
		# 	id='zoom-slider',
		# 	min=1,
		# 	max=15,
		# 	value=3,
		# 	marks={i: str(i) for i in range(1, 16)},
		# 	step=1
		# )
	])

	# # Define callback to update map zoom level
	# @dash.callback(
	# 	Output('map', 'figure'),
	# 	[Input('zoom-slider', 'value')]
	# )
	# def update_map(zoom_level):
	# 	fig.update_layout(mapbox=dict(zoom=zoom_level))
	# 	return fig

	return layout
# # Run the app
# if __name__ == '__main__':
# 	app.run_server(debug=True)
