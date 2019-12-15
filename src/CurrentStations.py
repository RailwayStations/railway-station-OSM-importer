import json

import requests


def getCurrentLastDatabaseIds(country_code):
    url = "https://api.railway-stations.org/{}/stations".format(country_code)
    print("Checking on the server: {}".format(url))
    response = requests.get(url=url)
    result = -1
    for station in response.json():
        if "id" in station:
            id = station["id"]
            if id > result:
                result = id
    return result
