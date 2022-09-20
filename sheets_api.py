"""
pip install --upgrade google-api-client google-auth-httplib2 google-auth-oauthlib
"""
import os
from Google import Create_Service
import app_config
import lol_api

CLIENT_SECRET_FILE = 'LeagueTrackerGoogle.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

sheets_data = lol_api.pull_league_data()

print(sheets_data[3][0])