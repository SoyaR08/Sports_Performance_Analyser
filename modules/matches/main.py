from .libraries import clean_matches
import os

def build_matches_environment():

    os.makedirs("final_data/tests/matches", exist_ok=True)

    matches_df = clean_matches("cleaned_data/cleaned_matches")
    matches_df.to_csv("final_data/tests/matches/matches.csv", index=False)