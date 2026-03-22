from .libraries import clean_matches
import os

def build_matches_environment():

    print("============ Módulo de Partidos ============")
    print("Creando carpeta....")
    os.makedirs("final_data/tests/matches", exist_ok=True)
    print("Carpeta Creada")
    matches_df = clean_matches("cleaned_data/cleaned_matches")
    print("Datos obtenidos")
    matches_df.to_csv("final_data/tests/matches/matches.csv", index=False)
    print("Archivo matches.csv")
    print("============ Fin de Módulo ============")