from datetime import datetime

def writeLog(gameID, message):
    lines = []

    #Get current file contents (Using with open(...) as ... automatically closes the file even when throwing errors)
    with open("LeagueTracker.log", "r") as logfile:
        lines = logfile.readlines()

    #Erase old file
    with open("LeagueTracker.log", "w") as logfile:
        logfile.write("")

    #Append data to log
    with open("LeagueTracker.log", "a") as logfile:
        if len(lines) >= 50:
            del lines[0]

         #Log current time and most recent game ID
        newline = datetime.now().strftime(f"%Y-%m-%d, %H:%M:%S -- gameID: {gameID} -- {message}\n")
        print(newline)
        lines.append(newline)

        for line in lines:
            logfile.write(line)