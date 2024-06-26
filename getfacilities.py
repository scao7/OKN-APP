import requests
import json
from dash import html
def json_to_layout(json_data):
    layout = []

    # Parse the JSON data
    data = json.loads(json_data)

    # Generate Dash components based on the JSON data
    for key, value in data.items():
        if isinstance(value, dict):
            layout.append(html.Div([
                html.H4(key),
                json_to_layout(json.dumps(value))
            ]))
        else:
            layout.append(html.Div([
                html.P(f"{key}: {value}")
            ]))
    
    return layout
def get_facility_website(api_key, facility_name_and_facility_address):
    # Define the Places API endpoint
    endpoint = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'

    # Define parameters for the API request
    params = {
        'key': api_key,
        'input': f'{facility_name_and_facility_address}',
        'inputtype': 'textquery',
        'fields': 'place_id'
    }

    # Make the API request to find the place ID
    response = requests.get(endpoint, params=params)
    data = response.json()
    place_id = None
    if 'candidates' in data:
        if len(data['candidates']) > 0:
            place_id = data['candidates'][0]['place_id']

    # If place ID is found, use it to get place details
    if place_id:
        details_endpoint = 'https://maps.googleapis.com/maps/api/place/details/json'
        details_params = {
            'key': api_key,
            'place_id': place_id,
            'fields': 'name,formatted_address,formatted_phone_number,website,opening_hours,rating'
        }

        # Make the API request to get place details
        details_response = requests.get(details_endpoint, params=details_params)
        details_data = details_response.json()
        return details_data