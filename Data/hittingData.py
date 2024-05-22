from pybaseball import batting_stats
import os
import json

# Team name mapping
team_name_mapping = {
    "ARI": "Arizona Diamondbacks",
    "ATL": "Atlanta Braves",
    "BAL": "Baltimore Orioles",
    "BOS": "Boston Red Sox",
    "CHC": "Chicago Cubs",
    "CHW": "Chicago White Sox",
    "CIN": "Cincinnati Reds",
    "CLE": "Cleveland Guardians",
    "COL": "Colorado Rockies",
    "DET": "Detroit Tigers",
    "MIA": "Miami Marlins",
    "HOU": "Houston Astros",
    "KCR": "Kansas City Royals",
    "LAA": "Los Angeles Angels",
    "LAD": "Los Angeles Dodgers",
    "MIL": "Milwaukee Brewers",
    "MIN": "Minnesota Twins",
    "NYM": "New York Mets",
    "NYY": "New York Yankees",
    "OAK": "Oakland Athletics",
    "PHI": "Philadelphia Phillies",
    "PIT": "Pittsburgh Pirates",
    "SDP": "San Diego Padres",
    "SFG": "San Francisco Giants",
    "SEA": "Seattle Mariners",
    "STL": "St. Louis Cardinals",
    "TBR": "Tampa Bay Rays",
    "TEX": "Texas Rangers",
    "TOR": "Toronto Blue Jays",
    "WSN": "Washington Nationals"
}

# Data Pull
data = batting_stats(2024, qual=50)

# Clean Data
ignore = ["Name", "IDfg", "Season", "Age", "Dol", "Age Rng", "G", "AB", "PA"]
data.drop(ignore, axis=1, inplace=True)
batting = data[data["Team"] != "- - -"]

# Replace team abbreviations with full team names
batting['Team'] = batting['Team'].replace(team_name_mapping)

team_batting_stats = batting.groupby("Team").mean().reset_index()

# Create a new Column/Value
team_batting_stats['xOP'] = (team_batting_stats['xBA'] + team_batting_stats['xSLG'] + team_batting_stats['BB%'] + team_batting_stats['AVG'] + team_batting_stats['OPS'])

xOP_baseline = team_batting_stats['xOP'].mean() - 1
team_batting_stats['xOP'] = team_batting_stats['xOP'] - xOP_baseline

# Convert the DataFrame to a dictionary with team names as keys
team_batting_stats_dict = team_batting_stats.set_index('Team').T.to_dict()

# Define the output file path within the project directory
json_file_path = os.path.join(os.getcwd(), 'team_batting_stats.json')

# Save the hitting data dictionary to a JSON file within the project directory
with open(json_file_path, 'w') as json_file:
    json.dump(team_batting_stats_dict, json_file, indent=4)
