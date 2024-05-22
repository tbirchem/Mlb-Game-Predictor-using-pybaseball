from pybaseball import pitching_stats
import json
import os

# Data Pull
data = pitching_stats(2024, qual=5)

# Keep only necessary columns
pitcher_stats = data[['Name', 'xERA', 'ERA', 'Stuff+']]

# Create a dictionary where pitcher names are keys and pitching statistics are values
pitcher_stats_dict = {}
for index, row in pitcher_stats.iterrows():
    pitcher_name = row['Name']
    pitcher_stats_dict[pitcher_name] = row.drop('Name').to_dict()

# Define the output file path within the project directory
json_file_path = os.path.join(os.getcwd(), 'sp_pitching_stats.json')

# Save the pitching data dictionary to a JSON file within the project directory
with open(json_file_path, 'w') as json_file:
    json.dump(pitcher_stats_dict, json_file, indent=4)







