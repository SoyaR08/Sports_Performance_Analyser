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