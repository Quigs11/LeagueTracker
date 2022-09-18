import app_config
import requests
import json

if __name__ == '__main__':
    # Create request url
    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/YungNutz?api_key=" + app_config.api_key

    # Submit GET request
    resp = requests.get(url)

    # Check status of GET request
    if resp.status_code != 200:
        raise Exception("GET  request failed with status code " + resp.status_code)

    # Print response
    resp_json = resp.json()
    print(resp_json)



