from .libraries import clean_matches, organise_files

def load_and_create_main_files():
    print("============ Carga y creación de datasets limpios ============")
    print(clean_matches(origin_path="data/matches/11", destiny_path="cleaned_data/cleaned_matches"))
    print(organise_files(origin_path="cleaned_data/lineups", destiny_path="cleaned_data/cleaned_lineups", match_folder="cleaned_data/cleaned_matches"))
    print(organise_files(origin_path="cleaned_data/events", destiny_path="cleaned_data/cleaned_events", match_folder="cleaned_data/cleaned_matches"))