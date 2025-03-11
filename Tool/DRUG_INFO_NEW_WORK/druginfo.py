import pandas as pd

file_paths = {
    'approved': 'data/approved.csv',
    'biotech': 'data/biotech.csv',
    'experimental': 'data/experimental.csv',
    'illicit': 'data/illicit.csv',
    'investigational': 'data/investigational.csv',
    'nutraceutical': 'data/nutraceutical.csv',
    'small molecule': 'data/small_molecule.csv',
    'withdrawn': 'data/withdrawn.csv'
}

target_data = {x: pd.read_csv(file_paths[x], index_col=0) for x in file_paths.keys()}

protein_ids_path = "data/protein_ids.txt"
with open(protein_ids_path) as f:
    protein_ids = [x.strip() for x in f.readlines()]

pharmacologically_active_data = pd.read_csv("data/pharmacologically_active.csv", index_col=0)
drug_pharmacological_map = {}
for row in pharmacologically_active_data.iterrows():
    if row[1]["UniProt ID"] not in protein_ids:
        continue
    drugs = [x.strip() for x in row[1]["Drug IDs"].split(";")]
    for drug in drugs:
        if drug not in drug_pharmacological_map:
            drug_pharmacological_map[drug] = set([row[1]["UniProt ID"]])
        else:
            drug_pharmacological_map[drug].add(row[1]["UniProt ID"])


def get_drug_info(uniprot_id):
    drugs = {}
    for class_, data in target_data.items():
        drugs[class_] = []
        drug_lists = data[data["UniProt ID"] == uniprot_id]["Drug IDs"].values
        for dl in drug_lists:
            drugs[class_].extend([x.strip() for x in dl.split(";")])
    
    drug_map = {}
    for class_, drug_list in drugs.items():
        for drug in drug_list:
            if drug not in drug_map:
                drug_map[drug] = set([class_])
            else:
                drug_map[drug].add(class_)

    return drug_map

def get_status(classes):
    status = [x for x in classes if (x != "small molecule" and x != "biotech" and x != "nutraceutical")]
    return ", ".join(status)
def get_type(classes):
    types = [x for x in classes if (x == "small molecule" or x == "biotech" or x == "nutraceutical")]
    return ", ".join(types)
def get_pharmacological_status(drug, uniprot_id):
    if drug in drug_pharmacological_map:
        if uniprot_id in drug_pharmacological_map[drug]:
            return "yes"
    return "unknown"

def get_comprehensive_drug_information(uniprot_id):
    drug_info = get_drug_info(uniprot_id)
    comprehensive_info = {}
    for drug, classes in drug_info.items():
        comprehensive_info[drug] = {
            "status": get_status(classes),
            "type": get_type(classes),
            "pharmacological action": get_pharmacological_status(drug, uniprot_id),
            'hlink': f"https://go.drugbank.com/drugs/{drug}"
        }
    return comprehensive_info

if __name__ == "__main__":
    uniprot_id = "P05067"
    for drugid, info in get_comprehensive_drug_information(uniprot_id).items():
        print(drugid, info)