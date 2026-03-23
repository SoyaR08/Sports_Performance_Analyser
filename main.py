from load import load_and_create_main_files
from modules.players import build_environment
from modules.events import build_events_environment
from modules.matches import build_matches_environment
from modules.teams import build_teams_environment
from analytics import build_leaderboards, add_player_info
import pandas as pd

if __name__ == "__main__":

    # Solo descomentar cuando se tengan todos los archivos del dataset StatsBomb Dataset
    # load_and_create_main_files()

    # build_teams_environment()
    # build_matches_environment()
    # build_events_environment()
    # build_environment()

    players_stats_df = pd.read_csv("final_data/players/players_events.csv")

    scorers, assistants, goalkeepers = build_leaderboards(players_stats_df, "final_data/players/players.csv")

    print("TOP GOLEADORES")
    print(scorers[["name", "goals"]].head(10))

    print("\nTOP ASISTENTES")
    print(assistants[["name", "assists"]].head(10))

    print("\nMEJORES PORTEROS")
    print(goalkeepers[["name", "saves_pm"]].head(10))