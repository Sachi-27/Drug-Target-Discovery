import requests 
import xml.etree.ElementTree as ET
import pandas as pd
import json

with open("protein_names.json") as f:
    protein_names = json.load(f)


# returns a list of pubmed ids in reverse order of publication date
def get_protein_info(uniprot_id, source, retrieve_amount=30, mindate=0, maxdate=2024):
    if source == "pubmed":
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
        print(search_term)  
        encoded_search_term = requests.utils.quote(search_term)
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax={retrieve_amount}&mindate={mindate}&maxdate={maxdate}&sort=pub+date&term={encoded_search_term}"
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

def get_pmid_info(pmid):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=xml"
    response = requests.get(url)
    tree = ET.fromstring(response.content)
    title = tree.findtext(".//Item[@Name='Title']")
    pub_year = tree.findtext(".//Item[@Name='PubDate']")
    authors = [author.text for author in tree.findall(".//Item[@Name='Author']")]
    doi = tree.findtext(".//Item[@Name='DOI']")
    link_from_doi = f"https://doi.org/{doi}"
    return {
        "title": title,
        "pub_year": pub_year,
        "authors": authors,
        "doi": doi,
        "link": link_from_doi
    }

if __name__ == '__main__':
    uniprot_id = 'P05067'
    source = 'pubmed'
    count, pubmed_ids = get_protein_info(uniprot_id, source, retrieve_amount=10, mindate=2014)
    print(count, pubmed_ids)

    # pmid_details = {}
    # for pmid in pubmed_ids:
    #     pmid_details[pmid] = get_pmid_info(pmid)
    #     print(pmid, pmid_details[pmid])
