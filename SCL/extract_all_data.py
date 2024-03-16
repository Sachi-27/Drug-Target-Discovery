import json

with open("../protein_properties/protein_props.json") as f:
    data = json.load(f)
    uniprot_human_proteins = list(data.keys())

import os

for protein in uniprot_human_proteins[17502:]:
    os.system(f"python3 xml-parser.py {protein}")
