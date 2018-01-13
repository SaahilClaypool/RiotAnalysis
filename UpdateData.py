from riotwatcher import RiotWatcher
import json
from time import sleep

w = RiotWatcher('21e6bb30-08e1-47ed-946f-cee514b740d8')

challenger = w.get_challenger()



# returns list of player id's in league
def getPlayerIds(league):
    entries = league['entries']
    l = []
    breakPoint = 0;
    for ent in entries:
        l.append(ent['playerOrTeamId'])
        ###comment out later
        #if(breakPoint > 1):
        #    break;
        #else:
        #    breakPoint +=1;
        ###comment out above
    return l

#returns the recent history of an ID
def getHistory(id):
    sleep(1)
    return w.get_recent_games(id)

#writes all games in recent history to own file
def writeAllGames(ids):
    playerNum = 0
    for id in ids: 
        hist = getHistory(id)
        gameids = getGameIds(hist)
        gamenum = 0
        for gameid in gameids:
            try:
                game = getGame(int(gameid))
                fileName = "Games/P" +str(playerNum)+"G"+ str(gamenum)+".txt"
                gamenum +=1
                file = open(fileName, 'w')
                file.write(json.dumps(game))
                file.close()
            except :
                print(gameid)
        playerNum +=1
#returns game object after sleeping
def getGame(gameid):
    sleep(1)
    game =  w.get_match(gameid, w.default_region, True)
    return game
#returns game id's from recent history
def getGameIds (hist):
    l = []
    for game in hist["games"]:
        l.append(game["gameId"])
    return l  

#print(w.get_match(2004556024, w.default_region, True))
#run
writeAllGames(getPlayerIds(challenger))
