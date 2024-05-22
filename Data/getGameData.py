import os
import requests
import json
import datetime


def get_todays_games():
    # Get today's date in YYYY-MM-DD format
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    # MLB GameDay API URL for the schedule
    url = f'https://statsapi.mlb.com/api/v1/schedule?sportId=1&hydrate=probablePitcher(note)&date={today}'

    response = requests.get(url)
    data = response.json()

    matchups = []

    for date in data['dates']:
        for game in date['games']:
            matchup = {}
            matchup['home_team'] = game['teams']['home']['team']['name']
            matchup['away_team'] = game['teams']['away']['team']['name']

            # Fetch the probable pitchers if available
            home_pitcher_info = game['teams']['home']['probablePitcher']
            if home_pitcher_info:
                matchup['home_pitcher'] = home_pitcher_info['fullName']
            else:
                matchup['home_pitcher'] = 'TBD'

            away_pitcher_info = game['teams']['away']['probablePitcher']
            if away_pitcher_info:
                matchup['away_pitcher'] = away_pitcher_info['fullName']
            else:
                matchup['away_pitcher'] = 'TBD'

            matchups.append(matchup)

    return matchups


def save_to_file(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    # Get today's MLB matchups
    matchups = get_todays_games()

    # Define the output file path within the project directory
    file_path = os.path.join(os.getcwd(), 'today_games.json')

    # Save the matchups to a JSON file within the project directory
    save_to_file(matchups, file_path)
