# NBA Sports Betting Using Machine Learning 🏀
<img src="https://github.com/kyleskom/NBA-Machine-Learning-Sports-Betting/blob/master/Screenshots/output.png" width="1010" height="292" />

A machine learning AI used to predict the winners and under/overs of NBA games. Takes all team data from the 2007-08 season to current season, matched with odds of those games, using a neural network to predict winning bets for today's games. Achieves ~75% accuracy on money lines and ~58% on under/overs. Outputs expected value for teams money lines to provide better insight. 
## Packages Used

Use Python 3.8. In particular the packages/libraries used are...

* Tensorflow - Machine learning library
* XGBoost - Gradient boosting framework
* Numpy - Package for scientific computing in Python
* Pandas - Data manipulation and analysis
* Colorama - Color text output
* Tqdm - Progress bars
* Requests - Http library
* Scikit_learn - Machine learning library

## Usage

<img src="https://github.com/kyleskom/NBA-Machine-Learning-Sports-Betting/blob/master/Screenshots/Expected_value.png" width="1010" height="424" />

Make sure all packages above are installed.

```bash
$ git clone https://github.com/kyleskom/NBA-Machine-Learning-Sports-Betting.git
$ cd NBA-Machine-Learning-Sports-Betting
$ pip3 install -r requirements.txt
$ python3 main.py -xgb
```
Enter under/over and odds for today's games.

## Contributing

All contributions welcomed and encouraged.

## Data

Odds data from here: https://www.sportsbookreviewsonline.com/scoresoddsarchives/nba/nba%20odds%202022-23.xlsx
(Change the URL)

NBA Data from here: https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguedashteamstats.md


## Refreshing the Model to Include More Recent Season Data

1. Run CleanupModel.py
2. Download most recent odds data from link above
3. Run Refresh_Data.py
4. Run Process_Odds_Data.py with the current season
5. Run Create_Games.py
6. Retrain Both Models
