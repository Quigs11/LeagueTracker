"""
pip install --upgrade google-api-client google-auth-httplib2 google-auth-oauthlib
"""
import os
from Google import Create_Service
import lol_api
import log

# Pull data from league api

# Connect to the Google sheet
spreadsheet_id = '1jrBrtiVtg94Btdb3Onqf9RY1OXX2OFnwKc6ji4m6VoI'

# Google API requirements
CLIENT_SECRET_FILE = 'LeagueTrackerGoogle.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Create the service
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def check_id(username):
    # Pull most recent Game ID from Google Sheet
    prev_id = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        majorDimension='COLUMNS',
        range='General Data!A:A'
    ).execute()

    # Pull updated data from Riot
    sheets_data = lol_api.pull_league_data(username)
    log.writeLog(sheets_data[0], f"Checking most recent game for {username}...")    
    
    # Check if Game ID exists in Column A
    newID = True
    for ID in prev_id['values'][0]:
        if sheets_data[0] == ID:
            newID = False

    # Check writing conditions and log reason for failures
    if newID:
        if len(sheets_data) > 5:
            # Write to Sheet if conditions are met
            write_general(sheets_data)
            write_player(sheets_data)
            log.writeLog(sheets_data[0], f"Added new record to sheets...")
        else:
            log.writeLog(sheets_data[0], f"Didn't add record, need 2 players but only had {len(sheets_data) - 4}...")
    else:
        log.writeLog(sheets_data[0], f"Didn't add record, gameID already exists...")


def write_general(sheets_data):
    # Give the data to write to General sheet
    worksheet_name = 'General Data!'
    cell_range_insert = 'A2'
    values = [(sheets_data[0], sheets_data[1], sheets_data[2], sheets_data[3])]

    value_range_body = {
        'majorDimension': 'ROWS',
        'values': values
    }

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        valueInputOption='USER_ENTERED',
        range=worksheet_name + cell_range_insert,
        body=value_range_body
    ).execute()


def write_player(sheets_data):
    # Loop to write to each player sheet
    n = len(sheets_data) - 4
    for i in range(0, n):
        player_name = sheets_data[4 + i][0]

        # Give the data to write to Player sheets
        worksheet_name = player_name + ' Data!'
        cell_range_insert = 'A2'
        values = [
            (sheets_data[1], sheets_data[4 + i][1], sheets_data[4 + i][2], sheets_data[4 + i][3], sheets_data[4 + i][4],
             sheets_data[4 + i][5], sheets_data[4 + i][6])]
        value_range_body = {
            'majorDimension': 'ROWS',
            'values': values
        }

        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            valueInputOption='USER_ENTERED',
            range=worksheet_name + cell_range_insert,
            body=value_range_body
        ).execute()
