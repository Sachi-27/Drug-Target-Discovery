import requests 
import xml.etree.ElementTree as ET
import pandas as pd
import json

with open("protein_names.json") as f:
    protein_names = json.load(f)


# returns a list of pubmed ids in reverse order of publication date
def get_protein_info(uniprot_id, source, search_for="uniprot_id", retrieve_amount=30):
    if source == "pubmed":
        if search_for == "uniprot_id":
            # Fetching XML data from the URL
            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax={retrieve_amount}&sort=pub+date&term={uniprot_id}"
        elif search_for == "druggability_info":
            if uniprot_id not in protein_names:
                # This case is not handled in this version -- these proteins have been moved from uniprot to uniparc
                return 0, []
            elif "shortNames" not in protein_names[uniprot_id]:
                protein_name = protein_names[uniprot_id]["fullName"]
                search_term = f'(({uniprot_id}[All Fields]) OR ({protein_name}[All Fields])) AND (druggability[All Fields] OR "drug target"[All Fields] OR inhibitor[All Fields] OR "protein target"[All Fields] OR "drug discovery"[All Fields] OR "drug binding"[All Fields] OR "drug interaction"[All Fields] OR "targeted therapy"[All Fields])'
            else:
                protein_name = protein_names[uniprot_id]["fullName"]
                alias_names = protein_names[uniprot_id]["shortNames"]
                search_term = f'(({uniprot_id}[All Fields]) OR ({protein_name}[All Fields]) '
                for alias in alias_names:
                    search_term += f'OR ({alias}[All Fields]) '
                search_term += f') AND (druggability[All Fields] OR "drug target"[All Fields] OR inhibitor[All Fields] OR "protein target"[All Fields] OR "drug discovery"[All Fields] OR "drug binding"[All Fields] OR "drug interaction"[All Fields] OR "targeted therapy"[All Fields])'
            encoded_search_term = requests.utils.quote(search_term)
            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax={retrieve_amount}&sort=pub+date&term={encoded_search_term}"

        response = requests.get(url)
        xml_data = response.text
        root = ET.fromstring(xml_data)
        counttag = root.find(".//Count")
        count = int(counttag.text)

        # Find and Extract content within <IdList> tag 
        pubmed_ids = []
        for idlist in root.findall(".//IdList"):
            for id in idlist.findall(".//Id"):
                pubmed_ids.append(id.text)
        return count, pubmed_ids
    else:
        raise Exception(f"Do not support source {source}")

if __name__ == '__main__':
    uniprot_id = 'P05067'
    source = 'pubmed'
    count, pubmed_ids = get_protein_info(uniprot_id, source, search_for="uniprot_id", retrieve_amount=30)
    print(count, pubmed_ids)
    count, pubmed_ids = get_protein_info(uniprot_id, source, search_for="druggability_info", retrieve_amount=30)
    print(count, pubmed_ids)