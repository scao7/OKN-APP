from geopy.geocoders import Nominatim,GoogleV3

# Initialize the geocoder
geolocator = Nominatim(user_agent="okn_application")

# Define the address
address = "1600 Amphitheatre Parkway, Mountain View, CA"

# Get the location
location = geolocator.geocode(address)

# Print latitude and longitude
if location:
    print(f"Address: {address}")
    print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
else:
    print("Location not found")
