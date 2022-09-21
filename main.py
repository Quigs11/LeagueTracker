import app_config
import lol_api
import sheets_api

if __name__ == '__main__':
    lol_data = lol_api.pull_league_data()
    print(lol_data)

    #sheets_api.write_data()
