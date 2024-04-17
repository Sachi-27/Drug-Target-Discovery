from extract import extract_ppi_info

f1 = open("extract3.log", "a")
with open("extract2.log") as f:
    i = 0
    for line in f:
        if "Failed" in line:
            try:
                uniprot_id = line.split(":")[-1].strip()
                print(f"{i}. Trying : {uniprot_id}")
                extract_ppi_info(uniprot_id)
                print(f"{i}. Successful : {uniprot_id}")
                f1.write(f"{i}. Successful : {uniprot_id}\n")
            except:
                print(f"{i}. Failed : {uniprot_id}")
                f1.write(f"{i}. Failed : {uniprot_id}\n")
        i += 1
f1.close()
