import pandas as pd
import json
import os

def create_teams_dataset(path):

    teams_dict = {}

    for file in os.listdir(path):
        if file.endswith(".json"):

            with open(os.path.join(path, file), encoding="UTF-8") as f:
                data = json.load(f)

            for element in data:

                team1 = element["home_team"]
                team2 = element["away_team"]

                teams_dict[team1["home_team_id"]] = team1["home_team_name"]
                teams_dict[team2["away_team_id"]] = team2["away_team_name"]

    df = pd.DataFrame([
        {"id": k, "name": v} for k, v in teams_dict.items()
    ])

    return df