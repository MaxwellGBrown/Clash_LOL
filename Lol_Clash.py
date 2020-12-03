"""Analyze summoners for clash scouting phase."""
from collections import Counter
import json

import requests

requests.get('https://na1.api.riotgames.com/lol/status/v3/shard-data?api_key=RGAPI-9edf8094-671f-4360-9f9a-ed388495c6e5')

# Change these as needed
summoner_name = 'McPiece'
api_key = 'RGAPI-3b754a5b-eb18-4024-95c7-48abdf94a8c4'

# Get account ids from summoner name
r = requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}')
r.json()

puuid = r.json()['puuid']
account_id = r.json()['accountId']
summoner_id = r.json()['id']

# Get rank for summoner name
r1 = requests.get(f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}')
r1.json()

# SoloQ information
soloq_tier = r1.json()[0]['tier']
soloq_div = r1.json()[0]['rank']
soloq_rank = soloq_tier +' '+ soloq_div
soloq_w = r1.json()[0]['wins']
soloq_l = r1.json()[0]['losses']
soloq_g = soloq_w + soloq_l
soloq_win_pct = round((soloq_w / soloq_g) * 100, 1)

# Flex information
flex_tier = r1.json()[1]['tier']
flex_rank = r1.json()[1]['rank']
flex_rank = flex_tier + ' ' + flex_rank
flex_w = r1.json()[1]['wins']
flex_l = r1.json()[1]['losses']
flex_g = flex_w + flex_l
flex_win_pct = round((flex_w / flex_g) * 100, 1)

# Print summary 
print('Summoner name: ' + summoner_name)
print(f'SoloQ: {soloq_rank} {soloq_win_pct}%')
print(f'Flex: {flex_rank} {flex_win_pct}%')


# Get match history for summoner name 
r2 = requests.get(f'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?api_key={api_key}')

# Get amount of games played in each role for past 100 games (includes ARAM / very inaccurate)
roles, lanes = [], []

for i in range(0,100):
    role = r2.json()['matches'][i]['role']
    roles.append(role)
    lane = r2.json()['matches'][i]['lane']
    lanes.append(lane)
    
num_supp = roles.count('DUO_SUPPORT')
num_adc = roles.count('DUO')
num_mid = lanes.count('MID')
num_jung = lanes.count('JUNGLE')
lanes.count('BOTTOM')
num_top = lanes.count('TOP')

pct_supp = round(num_supp / len(lanes) * 100,2)
pct_adc = round(num_adc / len(lanes) * 100,2)
pct_mid = round(num_mid / len(lanes) * 100,2)
pct_jung = round(num_jung / len(lanes) * 100,2)
pct_top = round(num_top / len(lanes) * 100,2)

print('Percentage of games played by role in past 100 (including ARAM):')
print(f'Top: {pct_top}')
print(f'Jungle: {pct_jung}')
print(f'Mid: {pct_mid}')
print(f'ADC: {pct_adc}')
print(f'Support: {pct_supp}')

####################################################################### dont use
# Create lists without ARAM games and another with only Clash
response = r2.json()
not_aram_games = [g for g in response['matches'] if g['queue']!=450] # isn't needed anymore
clash_games = [g for g in response['matches'] if g['queue']==700]    # isn't needed anymore
###########################################################################

# Get match history for past 100 games (not-ARAMs)
r5 = requests.get(f'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?queue=700&queue=400&queue=420&queue=430&api_key={api_key}')
not_aram_games = r5.json()['matches']
# Get amount of games played per role (no ARAM)
roles, lanes = [], []
for i in range(0,i):
    role = not_aram_games[i]['role']
    roles.append(role)
    lane = not_aram_games[i]['lane']
    lanes.append(lane)

# these are named the same as previously, probably bad as is, but ok if they're all defined in a function
num_supp = roles.count('DUO_SUPPORT')
num_adc = roles.count('DUO')
num_mid = lanes.count('MID')
num_jung = lanes.count('JUNGLE')
num_bot = lanes.count('BOTTOM')
num_top = lanes.count('TOP')

pct_supp = round(num_supp / len(lanes) * 100,2)
pct_adc = round(num_adc / len(lanes) * 100,2)
pct_mid = round(num_mid / len(lanes) * 100,2)
pct_jung = round(num_jung / len(lanes) * 100,2)
pct_top = round(num_top / len(lanes) * 100,2)

print('Percentage of games played by role in past 100 (not ARAM):')
print(f'Top: {pct_top}')
print(f'Jungle: {pct_jung}')
print(f'Mid: {pct_mid}')
print(f'ADC: {pct_adc}')
print(f'Support: {pct_supp}')

############################################################################
################### CLASH ANALYSIS #########################################

# Get match history for all Clash games
r3 = requests.get(f'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?queue=700&api_key={api_key}')
clash_hist = r3.json()['matches']

# Example of 1 match history
clash_hist[0]

# get role statistics for clash games
length = len(clash_hist)
roles, lanes, game_ids = [], [], []

for i in range(length):
    role = clash_hist[i]['role']
    roles.append(role)
    lane = clash_hist[i]['lane']
    lanes.append(lane)
    game_id = clash_hist[i]['gameId']
    game_ids.append(game_id)
    
num_supp = roles.count('DUO_SUPPORT')
num_adc = roles.count('DUO_CARRY')
num_mid = lanes.count('MID')
num_jung = lanes.count('JUNGLE')
num_top = lanes.count('TOP')

#list of game_ids for all clash games played
game_ids

# Most recent 10 played Clash games
# roles kind of inaccurate, might be best to just look at last 10 champs and role currently queued
roles = Counter(match["role"] for match in clash_hist)
lanes = Counter(match["lane"] for match in clash_hist)

print(f"Last 10 Clash games played for {summoner_name}:")
print(f"Top: {lanes.get('TOP', 0)}")
print(f"Jungle: {lanes.get('JUNGLE', 0)}")
print(f"Mid: {lanes.get('MID', 0)}")
print(f"ADC: {roles.get('DUO_CARRY', 0)}")
print(f"Support: {roles.get('DUO_SUPPORT', 0)}")
    
####################### SPECIFIC MATCH DETAILS ####################
game_id = 3665709273

r4 = requests.get(f'https://na1.api.riotgames.com/lol/match/v4/matches/{game_id}?api_key={api_key}')
r4.json()

# Accumulating stats into a list
game_details = r4.json()
stats = []
for index in range(10):
    stats.append({
        "name": game_details['participantIdentities'][index]['player']['summonerName'],
        "kill": game_details['participants'][index]['stats']['kills'],
        "death": game_details['participants'][index]['stats']['deaths'],
        "assist": game_details['participants'][index]['stats']['assists'],
        "win": game_details['participants'][index]['stats']['win'],
        "champ": game_details['participants'][index]['championId'],
    })

print(json.dumps(stats, indent=2))
