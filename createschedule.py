import sys
import csv
import random
import math
from functools import reduce
import itertools



def combineTeams(lista, listb) :
    results = []
    for team in listb:
        newList = listb.copy()
        returnList = []
        returnList.append(frozenset((lista[0], team)))
        #print(returnList)
        newList.remove(team)
        if len(newList) >= 1:
            gList = combineTeams(lista[1:], newList)
            #print(gList)

            for g in gList:
                results.append(returnList + g)
                #print(returnList)
        else:
            results.append(returnList)

    return(results)
        

def game_diff(g) :
    global records
    game = tuple(g)
    teama = game[0]
    teamb = game[1]
    diff = float(records[teama]) - float(records[teamb])
    return abs(diff)


records = {}

def main() :
    # Read in current week
    week = sys.argv[1]

    real_games = {}
    home_list = []
    away_list = []

    # Read in home/away real games
    ha = open("homeaway.txt", "r")
    ha_reader = csv.DictReader(ha)
    for row in ha_reader:
        read_week = row['week']
        home_team = row['home']
        away_team = row['away']
        real_games[home_team] = away_team
        real_games[away_team] = home_team
        if read_week == week:
            home_list.append(home_team)
            away_list.append(away_team)
        #real_games[home_team][away_team] = week

    print(real_games)
    print(home_list)
    print(away_list)
    print(len(home_list))

    # Read in already played
    ap = []
    alreadyFile = open("alreadyplayed.txt", "r")
    af_reader = csv.DictReader(alreadyFile)
    for row in af_reader:
        read_week = row['week']
        home_team = row['home']
        away_team = row['away']
        ap.append(frozenset((home_team, away_team)))

    # Read in records
    global records
    record_file = open("records.txt", "r")
    rf_reader = csv.DictReader(record_file)
    for row in rf_reader:
        team = row['team']
        wins = row['wins']
        records[team] = wins

    # Divide home/away into two groups
    home_group_1 = random.sample(home_list, k=math.ceil(len(home_list)/2))
    home_group_2 = list(set(home_list).difference(set(home_group_1)))
    away_group_1 = random.sample(away_list, k=math.ceil(len(away_list)/2))
    away_group_2 = list(set(away_list).difference(set(away_group_1)))
    print(home_group_1)
    print(home_group_2)
    print(away_group_1)
    print(away_group_2)

    # In each group itemize all combinations
    combos_1 = combineTeams(home_group_1, away_group_1)
    combos_2 = combineTeams(home_group_2, away_group_2)
    print(len(combos_1))
    print(len(combos_2))

    # Remove already played/scheduled games
    c1 = list(filter(lambda gs: not any(map(lambda v: frozenset(v) in gs, ap)) , combos_1))
    c2 = list(filter(lambda gs: not any(map(lambda v: frozenset(v) in gs, ap)) , combos_2))
    print(len(c1))
    print(len(c2))


    # Determine win diff
    r = (map(lambda glist: reduce(lambda x, y: x+y, map(game_diff, glist)), c1))
    #filter(
    lr = list(r)
    print(len(lr))
    min_val = min(lr)
    print(min_val)
    (r, c1) = filter(lambda x: x[0] == min_val , zip(lr, c1))
    print(c1)
    #print(list(map(game_diff, c1)))

# Pick the lowest win diff
# If Tied maximize real games, current week * 2
# If Tied minimize square of diffs
# If Tied random
    f1 = random.choice(c1)
    f2 = random.choice(c2)
    print(f1)
    print(f2)




if __name__ == '__main__' :
    main()
