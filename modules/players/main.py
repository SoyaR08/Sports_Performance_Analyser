from .libraries import *
import os

def build_environment():

    os.makedirs("final_data/tests4/players", exist_ok=True)

    player_events_df = getPlayerEvents("cleaned_data/cleaned_events")

    player_events_df.to_csv("final_data/tests4/players/players_events_try.csv", index=False)

    print("Archivo players_events_try.csv creado")

    player_minutes_df = getLineups("cleaned_data/cleaned_lineups")

    player_minutes_df.to_csv("final_data/tests4/players/players_minutes.csv", index=False)

    print("Archivo players_minutes.csv creado")