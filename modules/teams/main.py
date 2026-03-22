from .libraries import create_teams_dataset
import os

def build_teams_environment():

    os.makedirs("final_data/tests4/teams", exist_ok=True)
    df = create_teams_dataset("cleaned_data/cleaned_matches")
    df = df.sort_values("id")
    df.to_csv("final_data/tests4/teams/teams.csv", index=False)