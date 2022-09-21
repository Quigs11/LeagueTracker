import app_config
import requests
import datetime

#Dictionary of tracked players
playerlist = {
    "Conner" : "Quigls",
    "Andy" : "Jesus Juicy ",
    "Justin" : "YungNutz",
    "Josh" : "FORGEJackson",
    "Kyle" : "IronMagician"    
}

def get_request(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("GET request failed with status code " + str(resp.status_code))
    return resp.json()


def pull_league_data():
    # Get puuid by summoner id
    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/+" + app_config.summoner_id + "?api_key=" + decrypt_key(app_config.lak)
    puuid = get_request(url)['puuid']

    # Get most recent aram game
    url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?queue=450&api_key=" + decrypt_key(app_config.lak)
    game_id = get_request(url)[0]

    # Get aram game info
    url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + game_id + "?api_key=" + decrypt_key(app_config.lak)
    game_info = get_request(url)
    teams = game_info['info']['teams']
    participants = game_info['info']['participants']
    game_date_int = int(game_info['info']['gameEndTimestamp'])
    game_date = datetime.datetime.fromtimestamp(game_date_int / 1000).date()  # divide by 1000 to go from milliseconds to seconds

    # Determine which team is ours
    for p in participants:
        if p['puuid'] == puuid: 
            team_id = p['teamId']
            early_surrender = p['teamEarlySurrendered']
            for t in teams:
                if t['teamId'] == team_id:
                    team = t
            result = 'Win' if team['win'] else 'Lose'
            logging_info = [str(game_date), result, early_surrender]

    for p in participants:
        for name in playerlist:
            if p['summonerName'] == playerlist[name]:
                currentPlayer = [name, p['kills'], p['deaths'], p['assists'], p['totalTimeSpentDead'],p['totalDamageDealtToChampions']]
                logging_info.append(currentPlayer)

    return logging_info


def encrypt_key(key):
    res = ''
    character = '&'
    for c in key:
        res = res + c + character
    return res[::-1]


def decrypt_key(key):
    res = ''
    for c in key:
        if c != '&':
            res += c
    return res[::-1]
