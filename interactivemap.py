import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from urllib.request import urlopen
# get query infomation and update on the map 
from geopy.geocoders import Nominatim
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine, text, Column, Integer, String, Sequence
from getfacilities import get_facility_website
import os 
password = os.environ["okn_database"]
google_api_key=os.environ.get("GoogleMAP_API")
engine = create_engine(f'postgresql+psycopg2://postgres:{password}@127.0.0.1:5432/ONTO')
def create_map(data_scatter=None):	
	counties = json.load(open(r"Datasets\geojson-counties-fips.json",'r'))
	# df = pd.read_sql("SELECT rural_urban.rural_urban_code, rural_urban.rucc FROM public.rural_urban ORDER BY rural_urban_id ASC", engine)
	df = pd.read_sql("SELECT rural_urban.county_fips, rural_urban.rucc FROM public.rural_urban ORDER BY rural_urban_id ASC", engine)
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
	fig = px.choropleth_mapbox(df, geojson=counties, locations='county_fips', color='rucc',
							color_continuous_scale="Viridis",
							range_color=(1, 9),
							mapbox_style="open-street-map",
							zoom=5, center = {"lat": 33.2098, "lon": -87.5692}, 
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
	df = pd.read_sql(f'''SELECT 
		mh_treatment_provider.tp_name,
		mh_treatment_provider.tp_name_sub,
		mh_treatment_provider.address_line_1,
		mh_treatment_provider.address_line_2,
		mh_treatment_provider.state_code,
		city.city_name,
		mh_treatment_provider.latitude,
		mh_treatment_provider.longitude	  
		FROM 
			mh_treatment_provider
		JOIN 
			public.city ON mh_treatment_provider.city_id = city.city_id
		WHERE 
			mh_treatment_provider.zip_code = '{location}';''',engine)
	tp_name_list = df['tp_name'].tolist()
	tp_name_sub_list = df['tp_name_sub'].tolist()
	address_line_1_list= df['address_line_1'].tolist()
	address_line_2_list =df['address_line_2'].tolist()
	city_name_list = df['city_name'].tolist()
	state_list = df['state_code'].tolist()
	lon_list = df['longitude'].tolist()
	lat_list = df['latitude'].tolist()
	data_scatter =[]

	for name1,name2,street1,street2,city,state, la,lo in zip(tp_name_list, tp_name_sub_list,address_line_1_list,address_line_2_list,city_name_list,state_list,lat_list,lon_list):
		try:
			print(name1 + ','+ name2 + ',' + street1 + ','+ city + ',' + state)
			# la,lo = get_la_lo( street1+ ','+street2 + ','+ city + ',' + state)
			search_adress = name1 if name1!="NaN" else ""+ \
							name2 if name2!="NaN" else "" + \
							street1 if street1!="NaN" else "" + \
							street2 if street2!="NaN" else "" + \
							city if city!="NaN" else "" + \
							state if state!="NaN" else "" 
			# commented used the the google api, uncommented part directly access lat and lon in databas
			# web_info  =get_facility_website(google_api_key,search_adress)
			# la = web_info['result']['geometry']['location']['lat']
			# lo = web_info['result']['geometry']['location']['lng']
			data_scatter.append({'lat':la,'lon':lo,'name':name1,'info':search_adress})
		except:
			print("Not find the location")
		
	return data_scatter