from .libraries import create_teams_dataset
import os

# INPUT
INPUT_FOLDER = "cleaned_data"
MATCHES_INPUT_FOLDER = "cleaned_matches"

# OUTPUT
BASE_FOLDER = "final_data"
SPECIFIC_FOLDER = "teams"
FILENAME = "teams.csv"

# PATHS
BASE_FOLDER_PATH = os.path.join(BASE_FOLDER, SPECIFIC_FOLDER)
FILENAME_PATH = os.path.join(BASE_FOLDER_PATH, FILENAME)
INPUT_DATA_PATH = os.path.join(INPUT_FOLDER, MATCHES_INPUT_FOLDER)

def build_teams_environment():

    print("============ Módulo de Equipos ============")
    print("Creando carpeta....")
    os.makedirs(BASE_FOLDER_PATH, exist_ok=True)
    print("Carpeta Creada")

    print("Procesando datos...")
    df = create_teams_dataset(INPUT_DATA_PATH)

    print("Ordenando datos...")
    df = df.sort_values("id")

    print("Guardando archivo...")
    df.to_csv(FILENAME_PATH, index=False)

    print(f"Archivo {FILENAME} creado")
    print("============ Fin de Módulo ============")