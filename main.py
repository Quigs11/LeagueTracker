import app_config
import lol_api
import sheets_api
import log

if __name__ == '__main__':

    #lol_data = lol_api.pull_league_data()
    #print(lol_data)

    # Checks the previous game ID and writes new data
    sheets_api.check_id()

    log.writeLog(sheets_api.sheets_data[0])

