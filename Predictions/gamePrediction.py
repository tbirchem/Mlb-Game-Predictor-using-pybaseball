import json
import os
import re

def normalize_name(name):
    """Normalize the name by converting to lowercase and removing special characters."""
    return re.sub(r'\W+', '', name.lower())

def calculate_confidence(home_team_xOP, away_team_xOP, home_pitcher_xERA, away_pitcher_xERA):
    """Calculate the confidence of a prediction based on differences in xOP and xERA."""
    xOP_diff = abs(home_team_xOP - away_team_xOP)
    xERA_diff = abs(home_pitcher_xERA - away_pitcher_xERA)
    return xOP_diff + xERA_diff

def predict_game_winner(game, team_batting_stats, team_pitching_stats):
    # Normalize team and pitcher names
    home_team = normalize_name(game['home_team'])
    away_team = normalize_name(game['away_team'])
    home_pitcher = normalize_name(game['home_pitcher'])
    away_pitcher = normalize_name(game['away_pitcher'])

    # Check if teams and pitchers are in the stats dictionaries
    if home_team not in team_batting_stats or away_team not in team_batting_stats:
        print(f"Warning: One of the teams ({home_team}, {away_team}) not found in team_batting_stats")
        return None, None

    if home_pitcher not in team_pitching_stats or away_pitcher not in team_pitching_stats:
        print(f"Warning: One of the pitchers ({home_pitcher}, {away_pitcher}) not found in team_pitching_stats")
        return None, None

    # Get xOP and xERA for home and away teams
    home_team_xOP = team_batting_stats[home_team]['xOP']
    away_team_xOP = team_batting_stats[away_team]['xOP']
    home_pitcher_xERA = team_pitching_stats[home_pitcher]['xERA']
    away_pitcher_xERA = team_pitching_stats[away_pitcher]['xERA']

    # Calculate confidence based on differences in xOP and xERA
    confidence = calculate_confidence(home_team_xOP, away_team_xOP, home_pitcher_xERA, away_pitcher_xERA)

    # Predict the winner based on xOP and xERA comparison
    if home_team_xOP > away_team_xOP and home_pitcher_xERA < away_pitcher_xERA:
        return game['home_team'], confidence
    elif home_team_xOP < away_team_xOP and home_pitcher_xERA > away_pitcher_xERA:
        return game['away_team'], confidence
    elif home_team_xOP == away_team_xOP and home_pitcher_xERA < away_pitcher_xERA:
        return game['home_team'], confidence
    elif home_team_xOP == away_team_xOP and home_pitcher_xERA > away_pitcher_xERA:
        return game['away_team'], confidence
    else:
        # In case of ties or inconclusive predictions, return None
        return None, confidence

def predict_games(today_games, team_batting_stats, team_pitching_stats):
    predictions = []

    # Iterate over each game and predict the winner
    for game in today_games:
        winner, confidence = predict_game_winner(game, team_batting_stats, team_pitching_stats)
        if winner:
            predictions.append({
                'predicted_winner': winner,
                'confidence': confidence
            })

    # Sort predictions by confidence in descending order
    predictions.sort(key=lambda x: x['confidence'], reverse=True)

    return predictions

if __name__ == "__main__":
    # Load data from JSON files
    with open('/Users/taylorbirchem/PycharmProjects/Mlb Game Predictor/Data/today_games.json', 'r') as f:
        today_games = json.load(f)

    with open('/Users/taylorbirchem/PycharmProjects/Mlb Game Predictor/Data/team_batting_stats.json', 'r') as f:
        team_batting_stats = json.load(f)

    with open('/Users/taylorbirchem/PycharmProjects/Mlb Game Predictor/Data/sp_pitching_stats.json', 'r') as f:
        team_pitching_stats = json.load(f)

    # Normalize keys in the stats dictionaries
    team_batting_stats = {normalize_name(k): v for k, v in team_batting_stats.items()}
    team_pitching_stats = {normalize_name(k): v for k, v in team_pitching_stats.items()}

    # Predict game winners
    predictions = predict_games(today_games, team_batting_stats, team_pitching_stats)

    # Save predictions to a JSON file
    with open('game_predictions.json', 'w') as f:
        json.dump(predictions, f, indent=2)
