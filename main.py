from load import load_and_create_main_files
from modules.players import build_environment
from modules.events import build_events_environment
from modules.matches import build_matches_environment
from modules.teams import build_teams_environment
from analytics import build_leaderboards, add_player_info, plot_top_scorers, plot_top_assistants, plot_top_goalkeepers
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

    players_df = pd.read_csv("final_data/players/players.csv")
    players_minutes_df = pd.read_csv("final_data/players/players_minutes.csv")

    plot_top_scorers(scorers)

    plot_top_assistants(assistants)

    plot_top_goalkeepers(goalkeepers)
    
    