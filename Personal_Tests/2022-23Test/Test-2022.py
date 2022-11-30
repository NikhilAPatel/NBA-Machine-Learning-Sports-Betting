import xgboost as xgb
import copy
import numpy as np
import pandas as pd
from tqdm import tqdm

from src.Utils import Expected_Value
from src.Utils.Dictionaries import team_index_current, team_index_odds
from src.Utils.ModelSelector import select_XGB_Model
from src.Utils.tools import get_json_data, to_data_frame
from colorama import Fore, Style, init, deinit

data_url = 'https://stats.nba.com/stats/leaguedashteamstats?' \
           'Conference=&DateFrom=&DateTo={}&Division=&GameScope=&' \
           'GameSegment=&LastNGames=0&LeagueID=00&Location=&' \
           'MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&' \
           'PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&' \
           'PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&' \
           'Season=2022-23&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&' \
           'StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='


def calculateWinnings(odds):
    if odds > 0:
        return odds
    else:
        return 100 / abs(odds) * 100


init()
xgb_ml = xgb.Booster()
directory = "../../Models/Test/XGBoost_74.0%_ML-2.json"
xgb_ml.load_model(directory)

allgames = pd.read_excel("nba odds 2022-23Test.xlsx")
games = []

match_data = []
todays_games_uo = []
home_team_odds = []
away_team_odds = []
home_team_score = []
away_team_score = []

currentDate = '10%2F21%2F2022'
prevDate = '10%2F21%2F2022'
data = get_json_data(data_url.format(currentDate))
df = to_data_frame(data)

for i in tqdm(range(0, len(allgames), 2)):
    currentDateRaw = str(allgames.iloc[i]['Date'])
    currentDate = currentDateRaw[0:2] + '%2F' + currentDateRaw[2:] + '%2F2022'

    if(prevDate!=currentDate):
        data = get_json_data(data_url.format(currentDate))
        df = to_data_frame(data)
        prevDate = currentDate

    home_team = allgames.iloc[i + 1]['Team']
    away_team = allgames.iloc[i]['Team']
    games.append([home_team, away_team])

    todays_games_uo.append(1)

    home_team_odds.append(allgames.iloc[i + 1]['ML'])
    away_team_odds.append(allgames.iloc[i]['ML'])

    home_team_score.append(allgames.iloc[i + 1]['Final'])
    away_team_score.append(allgames.iloc[i]['Final'])

    home_team_series = df.iloc[team_index_odds.get(home_team)]
    away_team_series = df.iloc[team_index_odds.get(away_team)]
    stats = pd.concat([home_team_series, away_team_series])
    match_data.append(stats)

games_data_frame = pd.concat(match_data, ignore_index=True, axis=1)
games_data_frame = games_data_frame.T

frame_ml = games_data_frame.drop(columns=['TEAM_ID', 'CFID', 'CFPARAMS', 'TEAM_NAME'])
data = frame_ml.values
data = data.astype(float)

ml_predictions_array = []

for row in data:
    ml_predictions_array.append(xgb_ml.predict(xgb.DMatrix(np.array([row]))))

frame_uo = copy.deepcopy(frame_ml)
frame_uo['OU'] = np.asarray(todays_games_uo)
data = frame_uo.values
data = data.astype(float)

wincount = 0
losscount = 0
profit = 0
count = 0
for game in games:
    home_team = game[0]
    away_team = game[1]
    ev_home = float(Expected_Value.expected_value(ml_predictions_array[count][0][1], int(home_team_odds[count])))
    ev_away = float(Expected_Value.expected_value(ml_predictions_array[count][0][0], int(away_team_odds[count])))
    if ev_home > 0:
        print("Betting on {0} with EV {1}".format(home_team, ev_home))
        if (home_team_score[count] > away_team_score[count]):
            profit += calculateWinnings(home_team_odds[count])
            wincount += 1
            print(Fore.GREEN + 'Won-{0}'.format(profit) + Style.RESET_ALL)
        else:
            profit -= 100
            losscount += 1
            print(Fore.RED + 'Loss-{0}'.format(profit) + Style.RESET_ALL)

    if ev_away > 0:
        print("Betting on {0} with EV {1}".format(away_team, ev_away))
        if (home_team_score[count] < away_team_score[count]):
            profit += calculateWinnings(away_team_odds[count])
            wincount += 1
            print(Fore.GREEN + 'Won-{0}'.format(profit) + Style.RESET_ALL)
        else:
            profit -= 100
            losscount += 1
            print(Fore.RED + 'Loss-{0}'.format(profit) + Style.RESET_ALL)

    count += 1

print("\nWin Count: {0}\nLoss Count: {1}\nProfit: {2}".format(wincount, losscount, profit))

deinit()
