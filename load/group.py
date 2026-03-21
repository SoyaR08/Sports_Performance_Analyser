import pandas as pd
import shutil
import os

def filter_df(dataframe):

    df = dataframe.copy()

    # Extraer season_name del diccionario season
    df["season_name"] = df["season"].apply(lambda x: x["season_name"])

    # Separar la columna
    df[["season_start", "season_end"]] = df["season_name"].str.split("/", expand=True)

    # Si season_end es NaN (caso "2020"), poner el mismo valor que season_start
    df["season_end"] = df["season_end"].fillna(df["season_start"])

    # Convertir a número
    df["season_start"] = df["season_start"].astype(int)
    df["season_end"] = df["season_end"].astype(int)

    df = df[df["season_start"] >= 2000]

    df.reset_index(drop=True, inplace=True)

    return df

def get_match_id(match_folder, apply_filter=False):
    matches_dir = match_folder
    matches_list = []

    
    for file in os.listdir(matches_dir):
        if not file.endswith(".json"):
            continue

        if apply_filter:
            df = filter_df(pd.read_json(f"{matches_dir}/{file}"))
        else:
            df = pd.read_json(f"{matches_dir}/{file}")

        temp_list = df["match_id"].to_list()
        matches_list.extend(temp_list)

    return matches_list

def organise_files(origin_path, destiny_path, match_folder, apply_filter=False):

    # Carpeta donde organizar por competición
    destiny_folder = destiny_path

    # Crear la carpeta destino si no existe
    os.makedirs(destiny_folder, exist_ok=True)

    matches_list = get_match_id(match_folder, apply_filter)

    # Iterar sobre todos los archivos CSV
    for archivo in matches_list:

        filename = f"{archivo}.json"


        source = os.path.join(origin_path, filename)
        destination = os.path.join(destiny_folder, filename)

        if os.path.exists(source):
            # Mover el archivo
            shutil.move(source, destination)
    
    return "Archivos organizados con éxito"

def clean_matches(origin_path, destiny_path):

    os.makedirs(destiny_path, exist_ok=True)

    for file in os.listdir(origin_path):

        if not file.endswith(".json"):
            continue

        source = os.path.join(origin_path, file)

        df = pd.read_json(source)

        # aplicar filtro
        df = filter_df(df)

        if not df.empty:
            destination = os.path.join(destiny_path, file)

            df.to_json(destination, orient="records", indent=2, force_ascii=False)

    return "Partidos filtrados correctamente"

print(clean_matches(origin_path="data/matches/11", destiny_path="cleaned_data/cleaned_matches"))
print(organise_files(origin_path="cleaned_data/lineups", destiny_path="cleaned_data/cleaned_lineups", match_folder="cleaned_data/cleaned_matches"))
print(organise_files(origin_path="cleaned_data/events", destiny_path="cleaned_data/cleaned_events", match_folder="cleaned_data/cleaned_matches"))