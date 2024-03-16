import json

with open("../../protein_properties/protein_props.json") as f:
    data = json.load(f)
    uniprot_human_proteins = list(data.keys())
count = 0

# with open("initfact.txt") as f:
#     content = f.read()
#     for protein in uniprot_human_proteins:
#         if protein in content:
#             count += 1
#             # print(protein)

# print("Total uniprot human proteins: ", len(uniprot_human_proteins))
# print("Total number of human proteins with initfact: ", count)
# 33 human uniprot proteins with translation initiation factors

initfact_proteins = {}
prevline = None
with open("initfact.txt") as f:
    curr_class_name = None
    for line in f:
        line = line.strip()
        if "==" in line:
            curr_class_name = prevline
        else:
            if "(" in line:
                protein_id = line.split("(")[1].split(")")[0]
                if protein_id in uniprot_human_proteins:
                    if protein_id in initfact_proteins:
                        print("Haww")
                    else:
                        if(curr_class_name == "IF3 (IF-3)" or curr_class_name == "IF1 (IF-1)"):
                            class_type = "Prokaryotic"
                        else:
                            class_type = "Eukaryotic"
                        initfact_proteins[protein_id] = {"class": curr_class_name, "class_type": class_type}
        prevline = line

print("Total number of initfact uniprot human proteins: ", len(initfact_proteins))
# print(initfact_proteins)

with open("initfact_proteins.json", "w") as f:
    json.dump(initfact_proteins, f, indent=4)
