# folder = "cleaned_data/cleaned_events"   # carpeta donde están los json

# rows = []

# for file in os.listdir(folder):

#     if file.endswith(".json"):

#         match_id = file.replace(".json", "")

#         with open(os.path.join(folder, file), encoding="UTF-8") as f:
#             data = json.load(f)

#         for e in data:

#             event_type = e.get("type", {}).get("name")

#             if event_type not in ["Pass", "Shot"]:
#                 continue

#             row = {
#                 "match_id": match_id,
#                 "minute": e.get("minute"),
#                 "second": e.get("second"),
#                 "team": e.get("team", {}).get("name"),
#                 "player": e.get("player", {}).get("name"),
#                 "type": event_type
#             }

#             if event_type == "Pass":
#                 row["pass_outcome"] = e.get("pass", {}).get("outcome", {}).get("name")

#             if event_type == "Shot":
#                 row["shot_outcome"] = e.get("shot", {}).get("outcome", {}).get("name")

#             rows.append(row)

# df = pd.DataFrame(rows)

# df.to_csv("cleaned_data/test/test.csv", index=False)