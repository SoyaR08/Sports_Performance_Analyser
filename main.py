from load import load_and_create_main_files
from modules.players import build_environment
from modules.events import build_events_environment

if __name__ == "__main__":

    # Solo descomentar cuando se tengan todos los archivos del dataset StatsBomb Dataset
    # load_and_create_main_files()

    build_events_environment()
    build_environment()