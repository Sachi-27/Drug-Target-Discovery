import requests 
import xml.etree.ElementTree as ET
import pandas as pd

def get_protein_info(uniprot_id, source):
    if source == "pubmed":
        # Fetching XML data from the URL
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax=30&term={uniprot_id}"
        response = requests.get(url)
        xml_data = response.text

        # Parsing the XML data
        root = ET.fromstring(xml_data)

        # Find and Extract content within <IdList> tag 
        pubmed_ids = []
        for idlist in root.findall(".//IdList"):
            for id in idlist.findall(".//Id"):
                pubmed_ids.append(id.text)
        return pubmed_ids
    else:
        raise Exception(f"Do not support source {source}")

if __name__ == '__main__':
    uniprot_id = 'P05067'
    source = 'pubmed'
    pubmed_ids = get_protein_info(uniprot_id, source)
    print(pubmed_ids)