import json

with open("../../protein_properties/protein_props.json") as f:
    data = json.load(f)
    uniprot_human_proteins = list(data.keys())
count = 0

with open("intein.txt") as f:
    content = f.read()
    for protein in uniprot_human_proteins:
        if protein in content:
            count += 1
            print(protein)

print("Total uniprot human proteins: ", len(uniprot_human_proteins))
print("Total number of human proteins with intein: ", count)
# 0 human uniprot proteins with intein