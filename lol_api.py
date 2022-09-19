import app_config
import requests
import datetime

def get_request(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("GET request failed with status code " + str(resp.status_code))
    resp_json = resp.json()
    return resp_json

def pull_league_data():
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
    game_date_int = int(game_info['info']['gameEndTimestamp'])
    game_date = datetime.datetime.fromtimestamp(game_date_int / 1000).date()  # divide by 1000 to go from milliseconds to seconds

    # Determine which team is ours
    for p in participants:
        if p['puuid'] == puuid:
            team_id = p['teamId']
            early_surrender = p['teamEarlySurrendered']
            conner = p
        if p['summonerName'] == 'YungNutz':
            justin = p
        if p['summonerName'] == 'FORGEJackson':
            josh = p
        if p['summonerName'] == 'Jesus Juicy ':
            andrew = p
    for t in teams:
        if t['teamId'] == team_id:
            team = t
            break
    result = 'Win' if team['win'] else 'Lose'

    # Initialize logging structures in case any player is not present
    conner_log = ['Conner', '', '', '', '']
    andy_log = ['Andy', '', '', '', '']
    justin_log = ['Justin', '', '', '', '']
    josh_log = ['Josh', '', '', '', '']

    # Build logging structures
    # Player structure [NAME, KILLS, DEATHS, ASSISTS, TIME_SPENT_DEAD, DMG_TO_CHAMPIONS]
    try:
        conner_log = ['Conner', conner['kills'], conner['deaths'], conner['assists'], conner['totalTimeSpentDead'],
                      conner['totalDamageDealtToChampions']]
    except NameError:
        print('Conner not found')
    try:
        andy_log = ['Andy', andrew['kills'], andrew['deaths'], andrew['assists'], andrew['totalTimeSpentDead'],
                    andrew['totalDamageDealtToChampions']]
    except NameError:
        print('Andy not found')
    try:
        justin_log = ['Justin', justin['kills'], justin['deaths'], justin['assists'], justin['totalTimeSpentDead'],
                      justin['totalDamageDealtToChampions']]
    except NameError:
        print('Justin not found')
    try:
        josh_log = ['Josh', josh['kills'], josh['deaths'], josh['assists'], josh['totalTimeSpentDead'],
                    josh['totalDamageDealtToChampions']]
    except NameError:
        print('Josh not found')

    logging_info = [str(game_date), result, early_surrender, conner_log, andy_log, justin_log, josh_log]
    return logging_info
