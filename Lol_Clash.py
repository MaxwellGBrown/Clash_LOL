"""Analyze summoners for clash scouting phase."""
from collections import Counter, defaultdict
import json

import requests


def standardize_roles(matches):
    """Standardize bot lane roles/lanes into one value."""
    for match in matches:
        # print("lane: {lane}, role: {role}".format(**match))
        if match["lane"] == "NONE" or match["lane"] == "BOTTOM":
            if match["role"] in ["DUO_CARRY", "SOLO", "DUO"]:
                yield "ADC"
            elif match["role"] == "DUO_SUPPORT":
                yield "SUPPORT"
            else:
                print("Couldn't determine role for match {gameId} -"
                      " lane: {lane}, role: {role}".format(**match))
                yield match["role"]
        else:
            yield match["lane"]


def count_roles(matches):
    """Counts the roles played in provided matches."""
    roles = Counter(standardize_roles(matches))
    all_counts = defaultdict(lambda: 0)  # if there's no count of anything return 0
    all_counts.update(roles)
    return all_counts


def role_percentages_string(roles_tally):
    """Return a string that outlines role history in percentages."""
    role_keys = {
        "Top": "TOP",
        "Mid": "MID",
        "Jungle": "JUNGLE",
        "ADC": "ADC",  # adjusted to match standardize_roles() output
        "Support": "SUPPORT",  # adjusted to match standardize_roles() output
    } 

    total_matches = sum(roles_tally.values())

    output = []
    for title, key in role_keys.items():
        percentage = roles_tally[key] / total_matches
        output.append(f"{title}: {percentage:.2%}")

    return "\n".join(output)


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
print('Percentage of games played by role in past 100 (including ARAM):')
print(role_percentages_string(roles_tally))

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
print('Percentage of games played by role in past 100 (not ARAM):')
print(role_percentages_string(roles_tally))

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
print(role_percentages_string(roles_tally))
    
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
