import pandas as pd

def aggregate_players(df):

    stats = df.groupby("player_id").agg({
        "goals": "sum",
        "assists": "sum",
        "saves": "sum",
        "match_id": "count"
    }).rename(columns={"match_id": "matches"})

    return stats.fillna(0)

def top_scorers(stats, n=10):

    return stats.sort_values("goals", ascending=False).head(n)

def top_assistants(stats, n=10):

    return stats.sort_values("assists", ascending=False).head(n)

def top_goalkeepers(stats, n=10):

    gk = stats[stats["saves"] > 0].copy()

    gk["saves_pm"] = gk["saves"] / gk["matches"]

    return gk.sort_values("saves_pm", ascending=False).head(n)

def add_player_info(stats, players_path):

    players = pd.read_csv(players_path)

    stats = stats.merge(
        players,
        left_on="player_id",
        right_on="id",
        how="left"
    ).drop(columns=["id"])

    return stats

def build_leaderboards(df, players_path):

    stats = aggregate_players(df)

    scorers = top_scorers(stats)
    assistants = top_assistants(stats)
    goalkeepers = top_goalkeepers(stats)

    scorers = add_player_info(scorers, players_path)
    assistants = add_player_info(assistants, players_path)
    goalkeepers = add_player_info(goalkeepers, players_path)

    return scorers, assistants, goalkeepers