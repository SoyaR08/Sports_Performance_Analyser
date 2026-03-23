import pandas as pd
import json
import os

def clean_events(path):

    final_df = None
    summaries = []

    for file in os.listdir(path):

        if file.endswith(".json"):

            filepath = os.path.join(path, file)

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            df = pd.json_normalize(data)

            # Asegurar columnas
            for col in [
                "bad_behaviour.card.name",
                "foul_committed.card.name",
                "shot.outcome.name"
            ]:
                if col not in df.columns:
                    df[col] = None

            # Filtrar tiros
            shots = df[df["type.name"] == "Shot"]
            shots_on_target = shots[
                shots["shot.outcome.name"].isin(["Goal", "Saved", "Saved to Post"])
            ]
            goals = shots[shots["shot.outcome.name"] == "Goal"]  # <-- NUEVO

            # Tarjetas
            yellow_cards_fouls = df[
                (df["type.name"] == "Foul Committed") &
                (df["foul_committed.card.name"] == "Yellow Card")
            ]
            yellow_cards_behaviour = df[
                (df["type.name"] == "Bad Behaviour") &
                (df["bad_behaviour.card.name"] == "Yellow Card")
            ]
            red_cards = df[
                df["bad_behaviour.card.name"].isin(["Red Card", "Second Yellow"])
            ]

            match_id = file.replace(".json", "")

            # Agrupaciones
            shots_by_team = shots.groupby("team.id").size().reset_index(name="shots")
            shots_on_target_by_team = shots_on_target.groupby("team.id").size().reset_index(name="shots_on_target")
            goals_by_team = goals.groupby("team.id").size().reset_index(name="goals")
            yellow_by_team = pd.concat([yellow_cards_fouls, yellow_cards_behaviour]) \
                .groupby("team.id").size().reset_index(name="yellow_cards")
            red_by_team = red_cards.groupby("team.id").size().reset_index(name="red_cards")

            # Merge de todo
            summary = shots_by_team \
                .merge(shots_on_target_by_team, on="team.id", how="left") \
                .merge(goals_by_team, on="team.id", how="left") \
                .merge(yellow_by_team, on="team.id", how="left") \
                .merge(red_by_team, on="team.id", how="left")

            # Limpiar nulos
            summary = summary.fillna(0)

            # Convertir a int
            for col in ["shots", "shots_on_target", "goals", "yellow_cards", "red_cards"]:
                summary[col] = summary[col].astype(int)

            # Añadir match_id
            summary["match_id"] = match_id

            # Renombrar columna team.id -> team (como hacías antes)
            summary = summary.rename(columns={"team.id": "team"})

            summaries.append(summary)

    final_df = pd.concat(summaries, ignore_index=True, sort=False)
    return final_df