import json

with open("../../protein_properties/protein_props.json") as f:
    data = json.load(f)
    uniprot_human_proteins = list(data.keys())
count = 0

# 38 aatrnasy proteins
aatrnasy_proteins = {}
prev_line = None 
with open("aatrnasy.txt") as file:
    curr_class_name = None
    curr_class_num = None
    for line in file:
        line = line.strip()
        if "Class:" in line:
            curr_class_name = prev_line
            curr_class_num = line.split(" ")[-1]
        else:
            parts = line.split(" ")
            for part in parts:
                if "(" in part and ")" in part:
                    protein_id = part.strip()[1:-1]
                    if protein_id in uniprot_human_proteins:
                        if protein_id in aatrnasy_proteins:
                            print("HAWWW")
                            aatrnasy_proteins[protein_id].append({
                                "class_name": curr_class_name,
                                "class_num": curr_class_num
                            })
                        else:
                            aatrnasy_proteins[protein_id] = [{
                                "class_name": curr_class_name,
                                "class_num": curr_class_num
                            }]
        prev_line = line
        
print(len(aatrnasy_proteins))

with open("aatrnasy_proteins.json", "w") as f:
    json.dump(aatrnasy_proteins, f, indent=4)                