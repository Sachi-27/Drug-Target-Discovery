import json

with open("../../protein_properties/protein_props.json") as f:
    data = json.load(f)
    proteins = list(data.keys())

with open("extract.txt", "w") as file:
    prev_line = None
    with open("7tmrlist.txt") as f:
        curr_class = None
        for line in f:
            line = line.strip()
            if "==" in line:
                curr_class = prev_line
            elif "HUMAN" in line:
                file.write(f"{curr_class}::{line}\n")
            prev_line = line

# python3 7tmrlist.py > extract.txt

gpcr_proteins = {}
with open("extract.txt") as f:
    for line in f:
        line = line.strip()
        gpcr_class = line.split("::")[0]
        rest_line = line.split("::")[1].strip()
        rest_line = " ".join(rest_line.split("HUMAN")[1:]).strip()
        protein_id = rest_line.split(" ")[0].replace("(","").replace(")","")
        rest_line = " ".join(rest_line.split(" ")[1:]).strip()
        gpcr_name = rest_line.split("[")[0].strip()
        rest_line = " ".join(rest_line.split("[")[1:]).strip()
        gpcr_id = rest_line.split("]")[0].strip()
        gpcr_proteins[protein_id] = {
            "gpcr_class": gpcr_class,
            "gpcr_name": gpcr_name,
            "gpcr_id": gpcr_id
        }

print("Total GPCR proteins: ", len(gpcr_proteins))
with open("gpcr_proteins.json", "w") as f:
    json.dump(gpcr_proteins, f, indent=4)

# 825 GPCR proteins