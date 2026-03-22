from .libraries import clean_events
import os

def build_events_environment():

    print("============ Módulo de Eventos ============")
    print("Creando carpeta....")
    os.makedirs("final_data/tests4/events", exist_ok=True)
    print("Carpeta Creada")
    events_df = clean_events("cleaned_data/cleaned_events")
    print("Datos obtenidos")
    events_df.to_csv("final_data/tests4/events/events.csv", index=False)
    print("Archivo events.csv")
    print("============ Fin de Módulo ============")