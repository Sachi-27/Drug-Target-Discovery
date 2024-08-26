
import requests
import json

def get_proteindesc_info(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    response = requests.get(url)
    data = response.json()
    data = {uniprot_id: data["proteinDescription"]}
    with open(f"Desc/{uniprot_id}.json", "w") as f:
        json.dump(data, f, indent=4)
    
if __name__ == "__main__":
    with open("../protein_properties/protein_props.json") as f:
        uniprot_human_proteins = list((json.load(f)).keys())
with open("extract.log") as f:
    protein_names = f.readlines()
    protein_names = [x.split(",")[1].split(":")[1].strip() for x in protein_names]
    
    f = open("extract.log","a")
    for i, uniprot_id in enumerate(uniprot_human_proteins):
        if uniprot_id in protein_names:
            continue
        attempts = 0
        while True:
            if attempts == 3:
                f.write(f"{i}, Failed : {uniprot_id}\n")
                print(f"{i}, Failed : {uniprot_id}")
                break
            try:
                get_proteindesc_info(uniprot_id)
                f.write(f"{i}, Successful : {uniprot_id}\n")
                print(f"{i}, Successful : {uniprot_id}")
                break
            except:
                print(f"{i}, Reattempting : {uniprot_id}")
                attempts += 1
                

