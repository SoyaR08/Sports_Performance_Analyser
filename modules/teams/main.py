from .libraries import create_teams_dataset
import os

def build_teams_environment():

    print("============ Módulo de Equipos ============")
    print("Creando carpeta....")
    os.makedirs("final_data/tests4/teams", exist_ok=True)
    print("Carpeta Creada")
    df = create_teams_dataset("cleaned_data/cleaned_matches")
    print("Datos obtenidos")
    df = df.sort_values("id")
    df.to_csv("final_data/tests4/teams/teams.csv", index=False)
    print("Archivo teams.csv creado")
    print("============ Fin de Módulo ============")