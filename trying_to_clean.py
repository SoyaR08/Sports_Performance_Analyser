from datetime import time
import pandas as pd
import json
import os

def create_players_dataset(path):

    players_list = []
    for file in os.listdir(path):

        if file.endswith(".json"):

            with open(os.path.join(path, file), encoding="UTF-8") as f:
                data = json.load(f)

            team1 = data[0]
            team2 = data[1]


            for player in team1["lineup"]:

                cleaned_player = {
                    "id": player.get("player_id"),
                    "name": player.get("player_nickname") if player.get("player_nickname") != None else player.get("player_name"),
                    "country": player.get("country", {}).get("name")
                }

                players_list.append(cleaned_player)

            for player in team2["lineup"]:

                cleaned_player = {
                    "id": player.get("player_id"),
                    "name": player.get("player_nickname") if player.get("player_nickname") != None else player.get("player_name"),
                    "country": player.get("country", {}).get("name")
                }

                players_list.append(cleaned_player)

    df = pd.DataFrame(players_list)

    df = df.drop_duplicates(subset="id")

    return df

def clean_matches(path):

    final_df = None
    dfs = []

    for file in os.listdir(path):

        if file.endswith(".json"):

            filepath = os.path.join(path, file)

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            df = pd.DataFrame(data)

            df["home_team"] = df["home_team"].apply(lambda x: x.get("home_team_name") if isinstance(x, dict) else None)
            df["away_team"] = df["away_team"].apply(lambda x: x.get("away_team_name") if isinstance(x, dict) else None)
            df["kick_off"] = df["kick_off"].apply(
                lambda x: time.fromisoformat(x).strftime("%H:%M") if isinstance(x, str) else None
            )

            columns_to_delete = [
                "season", "match_status_360", "last_updated", "last_updated_360", "competition_stage",
                "stadium", "referee", "competition", "metadata", "match_status"
            ]

            df = df.drop(columns=columns_to_delete, errors="ignore")

            dfs.append(df)

    final_df = pd.concat(dfs, ignore_index=True, sort=False)

    return final_df

# os.makedirs("datasets/players", exist_ok=True)
os.makedirs("datasets/tests/matches", exist_ok=True)
os.makedirs("datasets/matches", exist_ok=True)

# df = create_players_dataset("cleaned_data/cleaned_lineups")
# df = df.sort_values("id")
# df.to_csv("datasets/players/players.csv", index=False)

matches_df = clean_matches("cleaned_data/cleaned_matches")
matches_df.to_csv("datasets/matches/matches.csv", index=False)