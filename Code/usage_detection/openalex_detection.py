import requests
import numpy as np
import csv


def doi_to_openAlexId(doi):
    """
    Convert a DOI to OpenAlex ID used as value in some API field such as "referenced_works"
    @param
        - doi: the doi to convert
    @return
        The OpenAlex ID if the DOI is in OpenAlex database, None otherwise
    """
    base_url = f"https://api.openalex.org/works/doi:{doi}"
    r = requests.get(base_url)
    if r.status_code == 200:
        r_json = r.json()
        return r_json["id"]
    else:
        return None

def load_datasets_info():
    """
    Load datasets information from csv at /Resources/data/datasets.csv and convert the doi to openalex_id
    @return:
        -dictionnary with dataset name as key and dictionary of information as value
    """
    datasets_info = {}
    with open('./Resources/data/datasets.csv') as ds_csv:
        ds_reader = csv.DictReader(ds_csv)
        for ds in ds_reader:
            datasets_info[ds["name"]] = {
                                            "doi":ds["doi"],
                                            "aliases":ds["aliases"].split(","),
                                            "openalex_id":doi_to_openAlexId(ds["doi"])
                                         }
    return datasets_info

def load_openalex_extraction_results():
    """
    Load papers information from /Results/extraction/papers_infos_openalex.csv obtained with openalex 
    @return:
        -list of dictionnary with paper information
    """
    papers_info = []
    with open("./Results/extraction/papers_infos_openalex.csv") as oa_info_csv:
        reader = csv.DictReader(oa_info_csv)
        for paper in reader:
            papers_info.append(paper)
    return papers_info

def reference_extraction(datasets_info,papers_info):
    opanalexID_to_name = {datasets_info[ds_name]["openalex_id"]:ds_name for ds_name in datasets_info}
    oa_IDs = set(opanalexID_to_name.keys())
    papers_datasets_reference = []
    for paper in papers_info:
        paper_ds_reference = {"doi":paper["doi"],"name":paper["title"]}
        for oa_id in oa_IDs:
            if oa_id in paper["references"]:
                paper_ds_reference[opanalexID_to_name[oa_id]] = True
            else:
                paper_ds_reference[opanalexID_to_name[oa_id]] = False
        papers_datasets_reference.append(paper_ds_reference)
    
    with open("./Results/extraction/oa_papers_datasets_reference.csv","w",newline="") as ao_ds_ref:
        fields = ["doi","name"]
        fields += [ds_name for ds_name in datasets_info]
        
        writer = csv.DictWriter(ao_ds_ref, fieldnames=fields)
        # Write the header row (column names)
        writer.writeheader()
        for paper in papers_datasets_reference:
            writer.writerow(paper)
    return papers_datasets_reference

def abstract_extraction(datasets_info,papers_info):
    papers_abstract_citation = []
    for paper in papers_info:
        paper_ds_abstract = {"doi":paper["doi"],"name":paper["title"]}
        abstract = paper["abstract"]
        for ds_name in datasets_info:
            paper_ds_abstract[ds_name] = False
            if ds_name in abstract:
                paper_ds_abstract[ds_name] = True
            else:    
                aliases = datasets_info[ds_name]["aliases"]
                for alias in aliases:
                    if alias in abstract:
                        paper_ds_abstract[ds_name] = True
                        break
        papers_abstract_citation.append(paper_ds_abstract)

    with open("./Results/extraction/oa_papers_datasets_abstract.csv","w",newline="") as ao_ds_ref:
        fields = ["doi","name"]
        fields += [ds_name for ds_name in datasets_info]
        
        writer = csv.DictWriter(ao_ds_ref, fieldnames=fields)
        
        # Write the header row (column names)
        writer.writeheader()
        for paper in papers_abstract_citation:
            writer.writerow(paper)
    return papers_abstract_citation

def main():
    datasets_info = load_datasets_info()
    papers_info = load_openalex_extraction_results()
    papers_datasets_reference = reference_extraction(datasets_info,papers_info)
    papers_abstract_reference = abstract_extraction(datasets_info,papers_info)

    
if __name__ =="__main__":
    main()
