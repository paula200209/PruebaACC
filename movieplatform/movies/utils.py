import requests

def get_country_coordinates(country_name):

    api_key = '629c125817b84a9d914b533f1427779e'
    base_url = "https://api.opencagedata.com/geocode/v1/json" # URL API
    params = {
        'q': country_name,
        'key': api_key
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data['results']:
        location = data['results'][0]['geometry']
        return (location['lat'], location['lng'])
    else:
        return (None, None)