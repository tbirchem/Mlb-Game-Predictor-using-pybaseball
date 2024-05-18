from pybaseball import pitching_stats
import pandas as pd
from FilePath import pitchingDataPath

#Org Data Query
data = pitching_stats(2024, qual=5)

#Find Home and Away Pitchers Stats
home_pitcher = 'Tanner Houck'
away_pitcher = 'Chris Sale'

#Get Pitching Stats for Both Pitchers
home_pitcher_stats = data[data['Name'] == home_pitcher]
away_pitcher_stats = data[data['Name'] == away_pitcher]

#Combine Home and Away stats into one table
combined_stats = pd.concat([home_pitcher_stats, away_pitcher_stats])
combined_stats.reset_index(drop=True, inplace=True)

#Export Data to CSV
combined_stats.to_csv(pitchingDataPath, index=False)





