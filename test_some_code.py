import os
import json
import pandas as pd

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

os.makedirs("datasets/tests/players", exist_ok=True)

lineup_df = getPlayerEvents("cleaned_data/cleaned_events")

lineup_df.to_csv("datasets/tests/players/players_events_try.csv", index=False)