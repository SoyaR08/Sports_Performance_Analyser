from .libraries import clean_matches
import os

INPUT_FOLDER = "cleaned_data"
MATCHES_INPUT_FOLDER = "cleaned_matches"

BASE_FOLDER = "final_data"
SPECIFIC_FOLDER = "matches"
FILENAME = "matches.csv"

BASE_FOLDER_PATH = os.path.join(BASE_FOLDER, SPECIFIC_FOLDER)
FILENAME_PATH = os.path.join(BASE_FOLDER_PATH, FILENAME)
INPUT_DATA_PATH = os.path.join(INPUT_FOLDER, MATCHES_INPUT_FOLDER)

def build_matches_environment():

    print("============ Módulo de Partidos ============")
    print("Creando carpeta....")
    os.makedirs(BASE_FOLDER_PATH, exist_ok=True)
    print("Carpeta Creada")
    matches_df = clean_matches(INPUT_DATA_PATH)
    print("Datos obtenidos")
    matches_df.to_csv(FILENAME_PATH, index=False)
    print(f"Archivo {FILENAME}")
    print("============ Fin de Módulo ============")