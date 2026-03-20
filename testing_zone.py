import pandas as pd
import json
import os

period_minutes = {
    1: (0, 45),
    2: (45, 90),
    3: (90, 105),
    4: (105, 120)
}

def abreviatePosition(position):
    position_dict = {
        # Goalkeepers
        "Goalkeeper": "GK",

        # Defenders
        "Right Back": "RB",
        "Right Center Back": "RCB",
        "Center Back": "CB",
        "Left Center Back": "LCB",
        "Left Back": "LB",
        "Right Wing Back": "RWB",
        "Left Wing Back": "LWB",

        # Defensive Midfield
        "Right Defensive Midfield": "RDM",
        "Center Defensive Midfield": "CDM",
        "Left Defensive Midfield": "LDM",

        # Midfield
        "Right Midfield": "RM",
        "Right Center Midfield": "RCM",
        "Center Midfield": "CM",
        "Left Center Midfield": "LCM",
        "Left Midfield": "LM",

        # Attacking Midfield / Wings
        "Right Wing": "RW",
        "Right Attacking Midfield": "RAM",
        "Center Attacking Midfield": "CAM",
        "Left Attacking Midfield": "LAM",
        "Left Wing": "LW",

        # Forwards
        "Right Center Forward": "RCF",
        "Striker": "ST",
        "Left Center Forward": "LCF",
        "Secondary Striker": "SS",
        "Center Forward": "CF",
    }

    # Devuelve la abreviatura si existe, sino devuelve el valor original
    return position_dict.get(position, position) if position else "[Match not played]" 

def time_to_minutes(t, period):
    if t is None:
        return period_minutes[period][1]
    minutes, seconds = map(int, t.split(":"))
    return period_minutes[period][0] + minutes

def minutes_played(position_entry):
    start = time_to_minutes(position_entry["from"], position_entry["from_period"])
    end = time_to_minutes(position_entry["to"], position_entry.get("to_period") or position_entry["from_period"])
    return max(0, end - start)

def getLineups(path):
    all_lineups = []

    for file in os.listdir(path):
        if not file.endswith(".json"):
            continue

        filepath = os.path.join(path, file)
        match_id = file.replace(".json", "")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        for team in data:  # Recorremos ambos equipos
            team_id = team.get("team_id")
            for player in team.get("lineup", []):
                # Abreviar posiciones
                player_positions = [
                    abreviatePosition(p["position"])
                    for p in player.get("positions", [])
                ]

                # Calcular minutos
                total_minutes = sum(minutes_played(p) for p in player.get("positions", []))

                all_lineups.append({
                    "player_id": player["player_id"],
                    # "player_name": player.get("name"),
                    "match_id": match_id,
                    "team_id": team_id,
                    "position_list": player_positions,
                    "minutes_played": total_minutes
                })

    return pd.DataFrame(all_lineups)

    

os.makedirs("datasets/tests/players", exist_ok=True)

lineup_df = getLineups("cleaned_data/cleaned_lineups")

lineup_df.to_csv("datasets/tests/players/players_minutes.csv", index=False)