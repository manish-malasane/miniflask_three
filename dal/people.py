import requests


def fetch_resource(resource):
    home_url = "https://swapi.dev"
    relative_url = f"/api/{resource}"
    absolute_url = home_url + relative_url
    response = requests.get(absolute_url)
    data = response.json()
    return data
