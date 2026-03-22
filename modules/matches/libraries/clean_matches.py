from datetime import time
import pandas as pd
import json
import os

def clean_matches(path):

    final_df = None
    dfs = []

    for file in os.listdir(path):

        if file.endswith(".json"):

            filepath = os.path.join(path, file)

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            df = pd.DataFrame(data)

            df["home_team"] = df["home_team"].apply(lambda x: x.get("home_team_id") if isinstance(x, dict) else None)
            df["away_team"] = df["away_team"].apply(lambda x: x.get("away_team_id") if isinstance(x, dict) else None)
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
