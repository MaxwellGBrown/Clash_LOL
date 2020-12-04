"""Analyze summoners for clash scouting phase."""
from collections import Counter, defaultdict
import json

import requests


def count_roles(matches):
    """Counts the roles played in provided matches."""
    roles = Counter(match["role"] for match in matches)
    lanes = Counter(match["lane"] for match in matches)

    all_counts = defaultdict(lambda: 0)  # if there's no count of anything return 0
    all_counts.update(roles)
    all_counts.update(lanes)
    return all_counts


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
matches = r2.json()["matches"]
roles_tally = count_roles(matches)

# TODO String formatting for percentages, because we enjoy fun
pct_supp = round(roles_tally["SUPPORT"] / len(matches) * 100,2)
pct_adc = round(roles_tally["ADC"] / len(matches) * 100,2)
pct_mid = round(roles_tally["MID"] / len(matches) * 100,2)
pct_jung = round(roles_tally["JUNGLE"] / len(matches) * 100,2)
pct_top = round(roles_tally["SUPPORT"] / len(matches) * 100,2)

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
roles_tally = count_roles(not_aram_games)

# TODO String formatting for percentages, because we enjoy fun
pct_supp = round(roles_tally["DUO_SUPPORT"] / len(not_aram_games) * 100,2)
pct_adc = round(roles_tally["DUO"] / len(not_aram_games) * 100,2)
pct_mid = round(roles_tally["MID"] / len(not_aram_games) * 100,2)
pct_jung = round(roles_tally["JUNGLE"] / len(not_aram_games) * 100,2)
pct_top = round(roles_tally["TOP"] / len(not_aram_games) * 100,2)

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

roles_tally = count_roles(clash_hist)

print(f"Last 10 Clash games played for {summoner_name}:")
print(f"Top: {roles_tally['TOP']}")
print(f"Jungle: {roles_tally['JUNGLE']}")
print(f"Mid: {roles_tally['MID']}")
print(f"ADC: {roles_tally['DUO_CARRY']}")
print(f"Support: {roles_tally['DUO_SUPPORT']}")
    
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
