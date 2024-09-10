import requests
from bs4 import BeautifulSoup as bs 
import pandas as pd

def get_drugbank_info(uniprot_id):
    url = f'https://go.drugbank.com/unearth/q?searcher=bio_entities&query={uniprot_id}'
    print(url)
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')

    links = soup.find_all('h2', class_='hit-link')
    print("Number of hit-links: ", len(links))
    drugs = {}
    for link_ in links:
        link = link_.find('a')
        link = link.get('href')
        new_url = 'https://go.drugbank.com' + link
        print(new_url)

        page2 = requests.get(new_url)
        soup2 = bs(page2.text, 'html.parser')
        table = soup2.find('table', id='target-relations')
        table = table.find('tbody')
        rows = table.find_all('tr')
        drugs_ = {}
        for row in rows:
            cols = row.find_all('td')
            # extract a tag from cols[0]
            hlink = cols[0].find('a')
            hlink = "https://go.drugbank.com" + hlink.get('href')
            drugbank_id = hlink.split('/')[-1]
            cols = [ele.text.strip() for ele in cols[:-1]]
            drugs_[drugbank_id] = {
                'drug_name': cols[0],
                'status': cols[1],
                'pharmacological action?': cols[3],
                'type': cols[4],
                'hlink': hlink
            }
        drugs[link] = drugs_
    return drugs


if __name__ == '__main__':
    uniprot_id = 'P05067'
    drugs = get_drugbank_info(uniprot_id)
    print(drugs)