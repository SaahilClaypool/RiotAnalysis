
from riotwatcher import RiotWatcher
import json
w = RiotWatcher('21e6bb30-08e1-47ed-946f-cee514b740d8')

# check if we have API calls remaining
print(w.can_make_request())

me = w.get_summoner(name='Lustboy')
#print(me)

# takes list of summoner ids as argument, supports up to 40 at a time
# (limit enforced on riot's side, no warning from code)
#my_mastery_pages = w.get_mastery_pages([me['id'], ])[str(me['id'])]
#print(my_mastery_pages)s
recentGames = w.get_match_list(me['id'])['matches']

print(json.dumps(recentGames))



lane15 = {"DUO_CARRY":float(0) , "DUO": float(0), "DUO_SUPPORT": float(0), "MID":float(0), "JUNGLE": float(0), "TOP": float(0),"SOLO": float(0)}
lane13 = {"DUO_CARRY":float(0) , "DUO": float(0), "DUO_SUPPORT": float(0),  "MID":float(0), "JUNGLE": float(0), "TOP": float(0), "SOLO": float(0)}
lane14 = {"DUO_CARRY":float(0) , "DUO": float(0), "DUO_SUPPORT": float(0), "MID":float(0), "JUNGLE": float(0), "TOP": float(0), "SOLO": float(0)}

g13 =0
g14 =0
g15 =0    

for i in recentGames:
    if(i["season"] == "SEASON2013"):
        if (i["lane"] == "BOTTOM"):
            if(i["role"] in lane13): 
                lane13[i["role"]] += 1;
        else:
            lane13[i["lane"]] += 1;    
        g13 += 1
    if(i["season"] == "SEASON2014"):
        if (i["lane"] == "BOTTOM"):
            if(i["role"] in lane14): 
                lane14[i["role"]] += 1;
        else:
           lane14[i["lane"]] += 1;    
        g14 += 1
    if(i["season"] == "SEASON2015"):
        if (i["lane"] == "BOTTOM"):
            if(i["role"] in lane15): 
                lane15[i["role"]] += 1;
        else:
            lane15[i["lane"]] += 1;    
        g15 += 1
for i in lane14:
    lane14[i] *= (1/g14)
for i in lane15:
    lane15[i] *= (1/g15)


print("14 season games : ", g14)
print(lane14)
print("15 season games : ", g15)
print(lane15)

# for i in recentGames['games']:
#     print (json.dumps(i, indent=2))
#     if(i['stats']['win']):
#         wins += 1; 
#     else: 
#         losses += 1;
#     games +=1

# print("wins = " , wins)
# print("losses = " , losses )

# returns a dictionary, mapping from summoner_id to mastery pages
# unfortunately, this dictionary can only have strings as keys,
# so must convert id from a long to a string
#print(my_mastery_pages)

#my_ranked_stats = w.get_ranked_stats(me['id'])
#print(my_ranked_stats)

#my_ranked_stats_last_season = w.get_ranked_stats(me['id'], season=3)
#print(my_ranked_stats_last_season)

## all static methods are prefaced with 'static'
## static requests do not count against your request limit
## but at the same time, they don't change often....
#static_champ_list = w.static_get_champion_list()
#print(static_champ_list)

## import new region code
#from riotwatcher import EUROPE_WEST

## request data from EUW
#froggen = w.get_summoner(name='froggen', region=EUROPE_WEST)
#print(froggen)

## create watcher with EUW as its default region
#euw = RiotWatcher('<your-api-key>', default_region=EUROPE_WEST)

## proper way to send names with spaces is to remove them, still works with spaces though
#xpeke = w.get_summoner(name='fnaticxmid')
#print(xpeke)

## Error checking requires importing LoLException as well as any errors you wish to check for.
##
## For Riot's API, the 404 status code indicates that the requested data wasn't found and
## should be expected to occur in normal operation, as in the case of a an invalid summoner name,
## match ID, etc.
##
## The 429 status code indicates that the user has sent too many requests
## in a given amount of time ("rate limiting").

#from riotwatcher import LoLException, error_404, error_429

#try:
#    response = rw.get_summoner('voyboy')
#except LoLException as e:
#    if e == error_429:
#        print('We should retry in {} seconds.'.format(e.headers['Retry-After']))
#    elif e == error_404:
#        print('Summoner not found.')
