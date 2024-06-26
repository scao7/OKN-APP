from getfacilities import get_facility_website
import json
import requests
import os
import pandas as pd
import numpy as np
google_api_key=os.environ.get("GoogleMAP_API")

df = pd.read_excel(r"D:\OKN_Front_End\Datasets\National_Directory_MH_Facilities_2022.xlsx", sheet_name=0)
street_list = df['street1'].tolist()
facility_list = df['name1'].tolist()
city_list = df['city'].tolist()
state_list = df['state'].tolist()
# print(street_list,facility_list)
data = []
# Write the header row
header = ["name","formatted_address","formatted_phone_number","website","opening_hours","rating"]

# Create a DataFrame for the header and write it to the CSV file
df_header = pd.DataFrame(columns=header)
filename = "Datasets/facility_info2.csv"
df_header.to_csv(filename, index=False, header=True, mode='w')


for street,name,city,state in zip(street_list, facility_list,city_list,state_list):
	web_info  =get_facility_website(google_api_key,name + ',' + street + ',' + city + ',' + state)
	print(web_info)

	if web_info:
		row = [web_info['result']['name'] if "name" in web_info['result'] else 'NaA',
			web_info['result']['formatted_address'] if "formatted_address" in web_info['result'] else 'NaA',
			web_info['result']['formatted_phone_number'] if "formatted_phone_number" in web_info['result'] else 'NaA',
			web_info['result']['website'] if "website" in web_info['result'] else 'NaA',
			web_info['result']['opening_hours'] if "opening_hours" in web_info['result'] else 'NaA',
			web_info['result']['rating'] if "rating" in web_info['result'] else 'NaA',
			]
	else:
		row = ['NaA','NaA','NaA','NaA','NaA','NaA']
	df_row = pd.DataFrame([row], columns=header)
	df_row.to_csv(filename, index=False, header=False, mode='a')
	
