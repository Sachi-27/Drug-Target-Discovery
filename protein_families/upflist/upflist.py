import json

with open("../../protein_properties/protein_props.json") as f:
    data = json.load(f)
    uniprot_human_proteins = list(data.keys())
count = 0

proteins_match = []
with open("upflist.txt") as f:
    content = f.read()
    for protein in uniprot_human_proteins:
        if protein in content:
            count += 1
            proteins_match.append(protein)

print("Total uniprot human proteins: ", len(uniprot_human_proteins))
print("Total number of human proteins with upflist: ", count)
# 210 human uniprot proteins with uncharacterised protein families

upf_proteins = {}
with open("upflist.txt") as f:
    curr_family = None
    curr_taxonomic_range = None
    curr_comments = None
    for line in f:
        line = line.strip()
        if line.startswith("Family:"):
            curr_family = line.split("Family:")[1].strip()
        elif line.startswith("Taxonomic range:"):
            curr_taxonomic_range = line.split("Taxonomic range:")[1].strip()
        elif line.startswith("Comments:"): 
            curr_comments = line.split("Comments:")[1].strip()
        else:
            for protein in proteins_match:
                if protein in line:
                    if curr_family in upf_proteins:
                        print("Ohh")
                        print(protein)
                    else:
                        upf_proteins[protein] = {"family": curr_family, "taxonomic_range": curr_taxonomic_range, "comments": curr_comments}

print("Total number of proteins with upflist: ", len(upf_proteins))

with open("upflist_proteins.json", "w") as f:
    json.dump(upf_proteins, f, indent=4)