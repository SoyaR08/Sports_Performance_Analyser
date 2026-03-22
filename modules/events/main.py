from .libraries import clean_events
import os

# INPUT
INPUT_FOLDER = "cleaned_data"
EVENTS_INPUT_FOLDER = "cleaned_events"

# OUTPUT
BASE_FOLDER = "final_data"
SPECIFIC_FOLDER = "events"
FILENAME = "events.csv"

# PATHS
BASE_FOLDER_PATH = os.path.join(BASE_FOLDER, SPECIFIC_FOLDER)
FILENAME_PATH = os.path.join(BASE_FOLDER_PATH, FILENAME)
INPUT_DATA_PATH = os.path.join(INPUT_FOLDER, EVENTS_INPUT_FOLDER)


def build_events_environment():

    print("============ Módulo de Eventos ============")
    print("Creando carpeta....")
    os.makedirs(BASE_FOLDER_PATH, exist_ok=True)
    print("Carpeta Creada")

    events_df = clean_events(INPUT_DATA_PATH)

    print("Datos obtenidos")
    events_df.to_csv(FILENAME_PATH, index=False)

    print(f"Archivo {FILENAME}")
    print("============ Fin de Módulo ============")