from libraries import *
import os

os.makedirs("final_data/tests/players", exist_ok=True)
os.makedirs("final_data/tests/players", exist_ok=True)

player_events_df = getPlayerEvents("cleaned_data/cleaned_events")

player_events_df.to_csv("final_data/tests/players/players_events_try.csv", index=False)


player_minutes_df = getLineups("cleaned_data/cleaned_lineups")

player_minutes_df.to_csv("final_data/tests/players/players_minutes.csv", index=False)