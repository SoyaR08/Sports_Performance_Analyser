import json
import pandas as pd
import os

# print(os.listdir("data/matches"))
path = "data/competitions.json"

with open(path, "r") as f:
    data = json.load(f)
    formated_data = {k : [match[k] for match in data] for k in data[0].keys()}
    df = pd.DataFrame(formated_data)

fields_to_drop = ["match_updated", "match_updated_360", "match_available_360", "match_available"]

df = df.drop(columns=fields_to_drop)

# df = df[df["competition_gender"] != "female"]
# df = df[df["competition_youth"] != True]

df = df[df["competition_id"] == 16]

# Separar la columna
df[["season_start", "season_end"]] = df["season_name"].str.split("/", expand=True)

# Si season_end es NaN (caso "2020"), poner el mismo valor que season_start
df["season_end"] = df["season_end"].fillna(df["season_start"])

# Convertir a número
df["season_start"] = df["season_start"].astype(int)
df["season_end"] = df["season_end"].astype(int)

df = df[df["season_start"] > 2000]

print(df)

df.reset_index(drop=True, inplace=True)
df.to_json("cleaned_data/clean_competitions.json", orient="records", indent=4)

# def clean_metadata(data):
#     for match in data:
#         if "metadata" in match:
#             del match["metadata"]

# with open(path, "r") as f:
#     data = json.load(f)
#     # clean_metadata(data)
#     chosen_match = data
#     keys = chosen_match[0].keys()
#     formated_data = {k : [match[k] for match in chosen_match] for k in keys}
#     df = pd.DataFrame(formated_data)

#     competition_df = pd.json_normalize(df["stadium"])

#     df = pd.concat([df.drop(columns=["stadium"]), competition_df], axis=1)

#     print(df.head())