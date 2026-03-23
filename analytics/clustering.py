from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def merge_datasets(stats_df, appearances_df):

    df = stats_df.merge(
        appearances_df,
        on=["player_id", "match_id", "team_id"],
        how="left"
    )

    return df

def build_player_features(df):

    grouped = df.groupby("player_id").agg({
        "goals": "sum",
        "assists": "sum",
        "saves": "sum",
        "yellow_cards": "sum",
        "red_cards": "sum",
        "minutes_played": "sum",
        "match_id": "count"
    }).rename(columns={"match_id": "matches"})

    grouped = grouped.fillna(0)

    return grouped

def add_per90_stats(df):

    df = df[df["minutes_played"] > 0]

    df["goals_p90"] = df["goals"] / df["minutes_played"] * 90
    df["assists_p90"] = df["assists"] / df["minutes_played"] * 90
    df["saves_p90"] = df["saves"] / df["minutes_played"] * 90

    df["cards_p90"] = (df["yellow_cards"] + df["red_cards"]) / df["minutes_played"] * 90

    return df


def run_clustering(df, features, k=4):

    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=k, random_state=42)
    df["cluster"] = kmeans.fit_predict(X_scaled)

    return df

def add_names(df, players_df):

    return df.merge(
        players_df,
        left_on="player_id",
        right_on="id",
        how="left"
    ).drop(columns=["id"])

def build_player_clusters(stats_df, appearances_df, players_df):

    df = merge_datasets(stats_df, appearances_df)

    df = df[df["minutes_played"] > 0]

    players = build_player_features(df)

    players = add_per90_stats(players)

    features = ["goals_p90", "assists_p90", "saves_p90", "cards_p90"]
    players_filtered = players[(players[features].sum(axis=1) > 0)].copy()
    players_filtered = run_clustering(players_filtered, features, k=3)

    players_filtered = add_names(players_filtered, players_df)

    return players_filtered