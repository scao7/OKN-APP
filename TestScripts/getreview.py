import requests
def get_coordinates(address, api_key):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(geocode_url)
    geocode_data = response.json()
    if geocode_data['status'] == 'OK':
        location = geocode_data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        raise Exception("Geocoding API request failed.")

def get_place_id(lat, lng, api_key):
    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=10&key={api_key}"
    response = requests.get(places_url)
    places_data = response.json()
    if places_data['status'] == 'OK':
        place_id = places_data['results'][0]['place_id']
        return place_id
    else:
        raise Exception("Places API request failed.")

def get_reviews(place_id, api_key):
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=reviews&key={api_key}"
    response = requests.get(details_url)
    details_data = response.json()
    if details_data['status'] == 'OK':
        return details_data['result']['reviews']
    else:
        raise Exception("Place Details API request failed.")
def get_website(place_id, api_key):
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=website&key={api_key}"
    response = requests.get(details_url)
    details_data = response.json()
    if details_data['status'] == 'OK':
        if 'website' in details_data['result']:
            return details_data['result']['website']
        else:
            print("No website found for this place.")
            return None
    else:
        raise Exception("Place Details API request failed.")

if __name__ == "__main__":
    address = "West Alabama Mental Health Center"
    api_key = "AIzaSyAra7tC7yiTJ0SHKh56YhShcnO3VHrXqcU"
    lat, lng = get_coordinates(address, api_key)
    place_id = get_place_id(lat, lng, api_key)
    web_info = get_website(place_id,api_key)
    try:
        reviews = get_reviews(place_id, api_key)
    except:
        reviews = ""
        print("reviews are empty")
    print(web_info)
    print(lat,lng,place_id)
    print(reviews)
    # for review in reviews:
    #     print(f"Author: {review['author_name']}")
    #     print(f"Rating: {review['rating']}")
    #     print(f"Review: {review['text']}")
    #     print("-----")
    # except Exception as e:
    #     print(e)
