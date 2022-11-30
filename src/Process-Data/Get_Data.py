from nba_api.stats.endpoints import leaguedashteamstats
import requests
import json
import pandas as pd
import os
from tqdm import tqdm
from src.Utils.tools import get_json_data, to_data_frame


# year = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
# season = ["2007-08", "2008-09", "2009-10", "2010-11", "2011-12", "2012-13", "2013-14", "2014-15", "2015-16", "2016-17",
#           "2017-18", "2018-19", "2019-20", "2020-21", "2021-22", "2022-23"]
season = ["2020-21", "2021-22", "2022-23"]
year = [2020, 2021, 2022, 2023]
month = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7]
days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]


begin_year_pointer = year[0]
end_year_pointer = year[0]
count = 0
year_count = 0


for season1 in tqdm(season):
    for month1 in tqdm(month):
        if month1 == 1:
            count += 1
            end_year_pointer = year[count]
        for day1 in tqdm(days):
            try:
                response = leaguedashteamstats.LeagueDashTeamStats(
                    team_id_nullable='0',
                    league_id_nullable='00',
                    season=str(season1),
                    date_from_nullable='10/29/'+str(begin_year_pointer),
                    date_to_nullable=str(month1)+'/'+str(day1)+'/'+str(end_year_pointer),
                    last_n_games='0',
                    opponent_team_id='0',
                    po_round_nullable='0',
                    pace_adjust='N',
                    per_mode_detailed='PerGame',
                    season_type_all_star='Regular Season',
                    two_way_nullable='0',
                    plus_minus='N',
                    rank='N',
                    measure_type_detailed_defense='Base',
                    month='0',
                    headers={'Accept': 'application/json, text/plain, */*',
                             'Accept-Encoding': 'gzip, deflate, br',
                             'Accept-Language': 'en-US,en;q=0.9',
                             'Connection': 'keep-alive',
                             'Host': 'stats.nba.com',
                             'Origin': 'https://www.nba.com',
                             'Referer': 'https://www.nba.com/',
                             'sec-ch-ua': '"Google Chrome";v="87", "\"Not;A\\Brand";v="99", "Chromium";v="87"',
                             'sec-ch-ua-mobile': '?1',
                             'Sec-Fetch-Dest': 'empty',
                             'Sec-Fetch-Mode': 'cors',
                             'Sec-Fetch-Site': 'same-site',
                             'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36',
                             'x-nba-stats-origin': 'stats',
                             'x-nba-stats-token': 'true'})
                general_df = response.get_data_frames()[0]


                general_df['Date'] = str(month1) + '-' + str(day1) + '-' + season1

                directory2 = os.fsdecode('../../Team-Data')

                isExist = os.path.exists(directory2 + '/' + str(season1))
                if not isExist:
                    os.makedirs(directory2 + '/' + str(season1))

                name = directory2 + '/' + str(season1) + '/' + str(month1) + '-' + str(day1) + '-' + season1 + '.xlsx'
                general_df.to_excel(name)
            except Exception as e:
                print(e)
                continue
    year_count += 1
    begin_year_pointer = year[count]


