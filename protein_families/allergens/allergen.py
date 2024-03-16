import json

with open("../../protein_properties/protein_props.json") as f:
    data = json.load(f)
    proteins = list(data.keys())

print("Total Uniprot proteins: ", len(proteins))

my_count = 0
my_proteins_uniprot = []
with open("allergen.txt") as f:
    entire_file = f.read()
    for protein in proteins:
        if protein in entire_file:
            my_count += 1
            my_proteins_uniprot.append(protein)

print("Total Uniprot proteins identified by me: ", my_count)
print(my_proteins_uniprot)

# uniprot_ids = ['O43290', 'P02538', 'Q13765', 'Q9BPX6', 'Q9BQE9']
# allergens = ["Hom s 1", "Hom s 5", "Hom s 2", "Hom s 4", "Hom s 3"]
# allergen_dict = dict(zip(uniprot_ids, allergens))

# print(allergen_dict)
# with open("allergen_dict.json", "w") as f:
#     json.dump(allergen_dict, f, indent=4)
