import pandas as pd
import json
import os

# Intervalos de minutos en cada parte del partido
period_minutes = {
    1: (0, 45),
    2: (45, 90),
    3: (90, 105),
    4: (105, 120)
}

# Abreviaturas oficiales del dataset para facilitar legibilidad
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

# Cambia el formato de los periodos para que se quede en 0 a 120
def time_to_minutes(t, period):
    if t is None:
        return period_minutes[period][1]
    minutes, seconds = map(int, t.split(":"))
    return period_minutes[period][0] + minutes

# Calcula los minutos totales
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


def getPlayerEvents(path):
    all_events = []

    for file in os.listdir(path):
        if not file.endswith(".json"):
            continue

        filepath = os.path.join(path, file)
        match_id = file.replace(".json", "")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        df = pd.json_normalize(data)

        # Asegurar columnas (clave para evitar errores)
        for col in [
            "shot.outcome.name",
            "pass.goal_assist",
            "foul_committed.card.name",
            "bad_behaviour.card.name",
            "goalkeeper.outcome.name"
        ]:
            if col not in df.columns:
                df[col] = None

        # GOLES
        goals = df[
            (df["type.name"] == "Shot") &
            (df["shot.outcome.name"] == "Goal")
        ]

        # ASISTENCIAS
        assists = df[df["pass.goal_assist"] == True]

        # AMARILLAS
        yellow_cards = df[
            (df["foul_committed.card.name"] == "Yellow Card") |
            (df["bad_behaviour.card.name"] == "Yellow Card")
        ]

        # ROJAS
        red_cards = df[
            df["bad_behaviour.card.name"].isin(["Red Card", "Second Yellow"])
        ]

        # PARADAS (goalkeeper saves)
        saves = df[
            (df["type.name"] == "Goal Keeper") &
            (df["goalkeeper.outcome.name"] == "Saved")
        ]

        # Agrupar por jugador
        goals_by_player = goals.groupby("player.id").size()
        assists_by_player = assists.groupby("player.id").size()
        yellow_by_player = yellow_cards.groupby("player.id").size()
        red_by_player = red_cards.groupby("player.id").size()
        saves_by_player = saves.groupby("player.id").size()

        # Unir todo
        summary = pd.DataFrame({
            "goals": goals_by_player,
            "assists": assists_by_player,
            "yellow_cards": yellow_by_player,
            "red_cards": red_by_player,
            "saves": saves_by_player
        }).fillna(0)

        summary["match_id"] = match_id
        summary = summary.reset_index().rename(columns={"player.id": "player_id"})

        all_events.append(summary)

    df_all = pd.concat(all_events, ignore_index=True, sort=False)

    cols = ["player_id", "goals", "assists", "yellow_cards", "red_cards", "saves"]

    df_all[cols] = df_all[cols].astype(int)

    # # Totales por jugador
    # totals = df_all.groupby("player_id", as_index=False).sum(numeric_only=True)

    return df_all