from .libraries import *
import os

# INPUT
INPUT_FOLDER = "cleaned_data"
EVENTS_INPUT_FOLDER = "cleaned_events"
LINEUPS_INPUT_FOLDER = "cleaned_lineups"

# OUTPUT
BASE_FOLDER = "final_data"
SPECIFIC_FOLDER = "players"

PLAYER_EVENTS_FILENAME = "players_events.csv"
PLAYER_MINUTES_FILENAME = "players_minutes.csv"
PLAYERS_FILENAME = "players.csv"

# PATHS
BASE_FOLDER_PATH = os.path.join(BASE_FOLDER, SPECIFIC_FOLDER)

PLAYER_EVENTS_PATH = os.path.join(BASE_FOLDER_PATH, PLAYER_EVENTS_FILENAME)
PLAYER_MINUTES_PATH = os.path.join(BASE_FOLDER_PATH, PLAYER_MINUTES_FILENAME)
PLAYERS_PATH = os.path.join(BASE_FOLDER_PATH, PLAYERS_FILENAME)

EVENTS_INPUT_PATH = os.path.join(INPUT_FOLDER, EVENTS_INPUT_FOLDER)
LINEUPS_INPUT_PATH = os.path.join(INPUT_FOLDER, LINEUPS_INPUT_FOLDER)


def build_environment():

    print("============ Módulo de Jugadores ============")
    print("Creando carpeta....")
    os.makedirs(BASE_FOLDER_PATH, exist_ok=True)
    print("Carpeta Creada")

    # Player events
    print("Procesando eventos de jugadores...")
    player_events_df = getPlayerEvents(EVENTS_INPUT_PATH)
    player_events_df.to_csv(PLAYER_EVENTS_PATH, index=False)
    print(f"Archivo {PLAYER_EVENTS_FILENAME} creado")

    # Player minutes
    print("Procesando minutos de jugadores...")
    player_minutes_df = getLineups(LINEUPS_INPUT_PATH)
    player_minutes_df.to_csv(PLAYER_MINUTES_PATH, index=False)
    print(f"Archivo {PLAYER_MINUTES_FILENAME} creado")

    # Players dataset
    print("Procesando dataset de jugadores...")
    players_df = create_players_dataset(LINEUPS_INPUT_PATH)
    players_df = players_df.sort_values("id")
    players_df.to_csv(PLAYERS_PATH, index=False)
    print(f"Archivo {PLAYERS_FILENAME} creado")

    print("============ Fin de Módulo ============")