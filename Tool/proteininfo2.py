import requests 
import xml.etree.ElementTree as ET
import pandas as pd
import json

with open("protein_names.json") as f:
    protein_names = json.load(f)

# returns a list of pubmed ids in reverse order of publication date
def get_protein_info(uniprot_id):
    if uniprot_id not in protein_names:
        # This case is not handled in this version -- these proteins have been moved from uniprot to uniparc
        return 0, []
    elif "shortNames" not in protein_names[uniprot_id]:
        protein_name = protein_names[uniprot_id]["fullName"]
        search_term = f'(("{uniprot_id}"[Title/Abstract] OR "{protein_name}"[Title/Abstract]) AND ((druggability[Title/Abstract] OR "drug target"[Title/Abstract] OR "protein target"[Title/Abstract] OR "drug discovery"[Title/Abstract] OR "drug binding"[Title/Abstract] OR "drug interaction"[Title/Abstract] OR "targeted therapy"[Title/Abstract]) OR ("cancer"[Title/Abstract] OR "tumor"[Title/Abstract] OR "neurodegenerative"[Title/Abstract] OR "disorders"[Title/Abstract] OR "metabolic disorders"[Title/Abstract] OR "cardiovascular"[Title/Abstract] OR "COPD"[Title/Abstract] OR "infectious"[Title/Abstract] OR "disease"[Title/Abstract])))'
    else:
        protein_name = protein_names[uniprot_id]["fullName"]
        alias_names = protein_names[uniprot_id]["shortNames"]
        search_term = f'(({uniprot_id}[Title/Abstract] OR "{protein_name}"[Title/Abstract])'
        for alias in alias_names:
            search_term += f' OR "{alias}"[Title/Abstract]'
        search_term += f') AND ((druggability[Title/Abstract] OR "drug target"[Title/Abstract] OR "protein target"[Title/Abstract] OR "drug discovery"[Title/Abstract] OR "drug binding"[Title/Abstract] OR "drug interaction"[Title/Abstract] OR "targeted therapy"[Title/Abstract]) OR ("cancer"[Title/Abstract] OR "tumor"[Title/Abstract] OR "neurodegenerative"[Title/Abstract] OR "disorders"[Title/Abstract] OR "metabolic disorders"[Title/Abstract] OR "cardiovascular"[Title/Abstract] OR "COPD"[Title/Abstract] OR "infectious"[Title/Abstract] OR "disease"[Title/Abstract]))'

    search_term += " AND Humans[MeSH Terms]" 
    encoded_search_term = requests.utils.quote(search_term)
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={encoded_search_term}&sort=date&filter=datesearch.y_10"
    return url

if __name__ == '__main__':
    uniprot_id = 'A1KXE4'
    url = get_protein_info(uniprot_id)
    print(url)
