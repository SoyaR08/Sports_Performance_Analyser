from .libraries import *
import os

def build_environment():

    print("============ Módulo de Jugadores ============")
    print("Creando carpeta....")
    os.makedirs("final_data/tests4/players", exist_ok=True)
    print("Carpeta Creada")
    player_events_df = getPlayerEvents("cleaned_data/cleaned_events")
    print("Datos obtenidos")
    player_events_df.to_csv("final_data/tests4/players/players_events_try.csv", index=False)

    print("Archivo players_events_try.csv creado")

    player_minutes_df = getLineups("cleaned_data/cleaned_lineups")
    print("Datos obtenidos")
    player_minutes_df.to_csv("final_data/tests4/players/players_minutes.csv", index=False)

    players_df = create_players_dataset("cleaned_data/cleaned_lineups")
    players_df = players_df.sort_values("id")
    players_df.to_csv("final_data/tests4/players/players.csv", index=False)

    print("Archivo players_minutes.csv creado")
    print("============ Fin de Módulo ============")