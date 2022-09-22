"""
pip install --upgrade google-api-client google-auth-httplib2 google-auth-oauthlib
"""
import os
from Google import Create_Service
import lol_api

# Pull data from league api
sheets_data = lol_api.pull_league_data()

# Connect to the Google sheet
spreadsheet_id = '1jrBrtiVtg94Btdb3Onqf9RY1OXX2OFnwKc6ji4m6VoI'

# Google API requirements
CLIENT_SECRET_FILE = 'LeagueTrackerGoogle.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Create the service
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def write_general():

    # Give the data to write to General sheet
    worksheet_name = 'General Data!'
    cell_range_insert = 'A2'
    values = [(sheets_data[0], sheets_data[1], sheets_data[2])]
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

def write_player():

    # Loop to write to each player sheet
    n = len(sheets_data)-3
    for i in range(0, n):

        player_name = sheets_data[3+i][0]

        # Give the data to write to Player sheets
        worksheet_name = player_name + ' Data!'
        cell_range_insert = 'A2'
        values = [(sheets_data[0], sheets_data[3+i][1], sheets_data[3+i][2], sheets_data[3+i][3], sheets_data[3+i][4],
                   sheets_data[3+i][5], sheets_data[3+i][6])]
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

