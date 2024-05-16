from pybaseball import batting_stats
from FilePath import filePath

#Data Pull
data = batting_stats(2024, qual=50)

#Clean Data
ignore = ["Name", "IDfg", "Season", "Age", "Dol", "Age Rng", "G", "AB", "PA"]
data.drop(ignore, axis=1, inplace=True)
batting = data[data["Team"] != "- - -"]

team_batting_stats = batting.groupby("Team").mean().reset_index()

#Create a new Column/Value
team_batting_stats['xOP'] = (team_batting_stats['xBA'] + team_batting_stats['xSLG'] + team_batting_stats['BB%'] + team_batting_stats['AVG'] + team_batting_stats['OPS'])

xOP_baseline = team_batting_stats['xOP'].mean() - 1
team_batting_stats['xOP'] = team_batting_stats['xOP'] - xOP_baseline

#Sort Data
team_batting_stats = team_batting_stats.sort_values(by="xOP", ascending=False)

team_batting_stats = team_batting_stats[['Team', 'xOP'] + [col for col in team_batting_stats if col not in ["Team", "xOP"]]]

team_batting_stats.to_csv(filePath, index=False)

print(team_batting_stats)