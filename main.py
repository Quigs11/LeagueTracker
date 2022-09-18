import app_config
import requests
import json
import datetime


def get_request(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("GET request failed with status code " + str(resp.status_code))
    resp_json = resp.json()
    return resp_json


if __name__ == '__main__':
    # Get puuid by summoner id
    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/+" + app_config.summoner_id + "?api_key=" + app_config.api_key
    puuid = get_request(url)['puuid']

    # Get most recent aram game
    url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?queue=450&api_key=" + app_config.api_key
    game_id = get_request(url)[0]

    # Get aram game info
    url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + game_id + "?api_key=" + app_config.api_key
    game_info = get_request(url)
    teams = game_info['info']['teams']
    participants = game_info['info']['participants']

    # Determine which team is ours
    for p in participants:
        if p['puuid'] == puuid:
            team_id = p['teamId']
            early_surrender = p['teamEarlySurrendered']
            break
    for t in teams:
        if t['teamId'] == team_id:
            team = t
            break
    result = 'Win' if team['win'] else 'Lose'

    # Build logging structure
    logging_info = [str(datetime.date.today()), result, early_surrender]
    print(logging_info)
