import requests

def get_facility_website(api_key, facility_name, facility_address):
    # Define the Places API endpoint
    endpoint = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'

    # Define parameters for the API request
    params = {
        'key': api_key,
        'input': f'{facility_name} {facility_address}',
        'inputtype': 'textquery',
        'fields': 'place_id'
    }
    print(params)
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
            'fields': 'website'
        }

        # Make the API request to get place details
        details_response = requests.get(details_endpoint, params=details_params)
        details_data = details_response.json()

        if 'result' in details_data:
            if 'website' in details_data['result']:
                return details_data['result']['website']

    return None

# Example usage
api_key = '88'
facility_name = 'MHCNCA Inc'
facility_address = 'Decatur/Morgan Counseling Center'
website = get_facility_website(api_key, facility_name, facility_address)

if website:
    print(f"Website of {facility_name}: {website}")
else:
    print(f"Website of {facility_name} not found.")
