import pandas as pd
import shutil
import os

def get_match_id():
    matches_dir = "data/matches/11"
    matches_list = []

    for file in os.listdir(matches_dir):
        df = pd.read_json(f"{matches_dir}/{file}")
        temp_list = df["match_id"].to_list()
        matches_list.extend(temp_list)

    return matches_list



# # Carpeta donde organizar por competición
carpeta_destino = "cleaned_data/events"

# # Crear la carpeta destino si no existe
os.makedirs(carpeta_destino, exist_ok=True)

matches_list = get_match_id()

# # Iterar sobre todos los archivos CSV
for archivo in matches_list:
        
    carpeta_origen = "data/events"

    filename = f"{archivo}.json"

    # Mover el archivo
    shutil.move(os.path.join(carpeta_origen, filename), os.path.join("cleaned_data/events", filename))




#print(os.listdir(matches_dir))