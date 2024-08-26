import os 
import json 

with open("../protein_properties/protein_props.json") as f:
    uniprot_human_proteins = list((json.load(f)).keys())

protein_names = {}
for uniprot_id in uniprot_human_proteins:
    try:
        with open(f"Desc/{uniprot_id}.json") as f:
            data = json.load(f)
            recommendedNames = {}
            
            if "fullName" in data[uniprot_id]["recommendedName"]:
                recommendedNames["fullName"] = data[uniprot_id]["recommendedName"]["fullName"]["value"]
            if "shortNames" in data[uniprot_id]["recommendedName"]:
                recommendedNames["shortNames"] = [x['value'] for x in data[uniprot_id]["recommendedName"]["shortNames"]]
        protein_names[uniprot_id] = recommendedNames
    except:
        continue

with open("protein_names.json", "w") as f:
    json.dump(protein_names, f, indent=4)