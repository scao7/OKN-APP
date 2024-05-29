import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from urllib.request import urlopen

from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine, text, Column, Integer, String, Sequence
import os 

def create_map(data_scatter=None):
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

	# Sample data for the scattermapbox layer
	# data_scatter = [
	# 	{'lat': 37.7749, 'lon': -122.4194, 'name': 'San Francisco'},
	# 	{'lat': 34.0522, 'lon': -118.2437, 'name': 'Los Angeles'},
	# 	{'lat': 40.7128, 'lon': -74.0060, 'name': 'New York City'},
	# ]
	# data_scatter = query_clinic()

	if data_scatter:
		# Create Scattermapbox trace
		scatter_trace = go.Scattermapbox(
			lat=[city['lat'] for city in data_scatter],
			lon=[city['lon'] for city in data_scatter],
			mode='markers',
			marker=dict(size=6, color='rgb(0, 0, 255)'),
			text=[city['name'] for city in data_scatter],
			hoverinfo='text'
		)

		fig.add_trace(scatter_trace)
		fig.update_layout(
			mapbox_center={"lat": data_scatter[0]['lat'], "lon": data_scatter[0]['lon']},
    		mapbox_zoom=11
		)

	# Define the layout
	layout = html.Div([
		dcc.Graph(id='map',figure=fig),
	])
	return layout

# get query infomation and update on the map 
from geopy.geocoders import Nominatim
def get_la_lo(address):

	# Initialize the geocoder
	geolocator = Nominatim(user_agent="okn_application")

	# Get the location
	location = geolocator.geocode(address)

	# Print latitude and longitude
	if location:
		print(f"Address: {address}")
		print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
	else:
		print("Location not found")
	return location.latitude,location.longitude

def query_clinic(location):
	# read the clinic list 
	df = pd.read_excel(r"D:\OKN_Front_End\Datasets\National_Directory_MH_Facilities_2022.xlsx", sheet_name=0)
	# print(location,)
	filterd = df[df['zip'] == int(location)]
	street_list = filterd['street1'].tolist()
	facility_list = filterd['name1'].tolist()
	city_list = filterd['city'].tolist()
	state_list = filterd['state'].tolist()
	# print(street_list,facility_list)
	data_scatter =[]

	for street,name,city,state in zip(street_list, facility_list,city_list,state_list):
		try:
			la,lo = get_la_lo(street + ',' + city + ',' + state)
			data_scatter.append({'lat':la,'lon':lo,'name':name,'info':street})
		except:
			print("Not find the location")
		

	return data_scatter
