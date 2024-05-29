import requests

# Define your Google Places API key
api_key = 'YOUR_GOOGLE_API_KEY'

# Function to get place details from an address
def get_place_details(api_key, address):
    # Get the place ID and location (latitude and longitude) from the address
    geocode_endpoint = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    geocode_params = {
        'input': address,
        'inputtype': 'textquery',
        'fields': 'place_id,geometry',
        'key': api_key
    }
    geocode_response = requests.get(geocode_endpoint, params=geocode_params)
    geocode_data = geocode_response.json()
    
    if geocode_data['status'] == 'OK':
        place_id = geocode_data['candidates'][0]['place_id']
        location = geocode_data['candidates'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        
        # Get the reviews and other place details using the place ID
        details_endpoint = f"https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            'place_id': place_id,
            'fields': 'name,rating,reviews',
            'key': api_key
        }
        details_response = requests.get(details_endpoint, params=details_params)
        details_data = details_response.json()
        
        if details_data['status'] == 'OK':
            place_details = details_data['result']
            return {
                'name': place_details['name'],
                'latitude': latitude,
                'longitude': longitude,
                'rating': place_details.get('rating'),
                'reviews': place_details.get('reviews', [])
            }
        else:
            print("No details found")
            return None
    else:
        print("Place not found")
        return None

# Define the address
address = "1600 Amphitheatre Parkway, Mountain View, CA"

# Get place details
place_details = get_place_details(api_key, address)

# Print the details
if place_details:
    print(f"Name: {place_details['name']}")
    print(f"Latitude: {place_details['latitude']}")
    print(f"Longitude: {place_details['longitude']}")
    print(f"Rating: {place_details['rating']}")
    for review in place_details['reviews']:
        print(f"Author: {review['author_name']}")
        print(f"Rating: {review['rating']}")
        print(f"Text: {review['text']}\n")
