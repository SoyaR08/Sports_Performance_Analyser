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

# folder = "cleaned_data/cleaned_events"   # carpeta donde están los json

# rows = []

# for file in os.listdir(folder):

#     if file.endswith(".json"):

#         match_id = file.replace(".json", "")

#         with open(os.path.join(folder, file), encoding="UTF-8") as f:
#             data = json.load(f)

#         for e in data:

#             event_type = e.get("type", {}).get("name")

#             if event_type not in ["Pass", "Shot"]:
#                 continue

#             row = {
#                 "match_id": match_id,
#                 "minute": e.get("minute"),
#                 "second": e.get("second"),
#                 "team": e.get("team", {}).get("name"),
#                 "player": e.get("player", {}).get("name"),
#                 "type": event_type
#             }

#             if event_type == "Pass":
#                 row["pass_outcome"] = e.get("pass", {}).get("outcome", {}).get("name")

#             if event_type == "Shot":
#                 row["shot_outcome"] = e.get("shot", {}).get("outcome", {}).get("name")

#             rows.append(row)

# df = pd.DataFrame(rows)

# df.to_csv("cleaned_data/test/test.csv", index=False)

os.makedirs("datasets/players", exist_ok=True)

df = create_players_dataset("cleaned_data/cleaned_lineups")
df = df.sort_values("id")
df.to_csv("datasets/players/players.csv", index=False)