import json, os

json_files = os.listdir("PDB")

data = {}

for file in json_files:
    with open(f"PDB/{file}") as f:
        data.update(json.load(f))
    
with open("pfb_info.json", "w") as f:
    json.dump(data, f, indent=4)

# 3.5 secs