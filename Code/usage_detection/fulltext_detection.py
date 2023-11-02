import pdf_utilities.pdf_utilities as pdf_util
import glob
import csv
import re
from tqdm import tqdm

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
                                            "title":ds["paper_title"],
                                            "name":ds["name"],
                                            "aliases":ds["aliases"].split(","),
                                            "url":ds["url"]
                                         }
    return datasets_info


def search_dataset_in_section(paper_path,section_name,dataset_infos,field="name"):
    res = {ds_name:False for ds_name in dataset_infos}
    try:
        text = pdf_util.extract_section(paper_path,section_name)
        if text:
            text = " ".join(text)
            for ds_name in dataset_infos:
                searched_str = dataset_infos[ds_name][field]
                if re.search(f"(?<![^_\\W]){searched_str}(?![^_\\s\\d\\.\\),'])",text):
                    res[ds_name] = True
                else:
                    for alias in dataset_infos[ds_name]["aliases"]:
                        if re.search(f"(?<![^_\\W]){alias}(?![^_\\s\\d\\.\\),'])",text):
                            res[ds_name] = True
                            break
    except:
        print(f"Unreadable paper:{paper_path}")
    
    return res
def main():
    #Load dataset_info
    ds_info = load_datasets_info()

    #Load list of downloaded pdf 
    papers_pdf_path = glob.glob("./Results/extraction/fulltext/INSIDE: Steering Spatial Attention with Non-imaging Information in CNNs*")
    data_csv = []
    
    print("Search in abstract started")
    for paper in tqdm(papers_pdf_path):
        paper_name = paper.split("/")[-1].removesuffix("pdf")
        #Get the abstract part
        search_res = search_dataset_in_section(paper,"abstract",ds_info)
        search_res["name"] = paper_name
        data_csv.append(search_res)
    
    # with open("./Results/extraction/fulltext_datasets_abstract.csv","w",newline="") as ft_ds_ref:
    #     fields = ["name"]
    #     fields += [ds_name for ds_name in ds_info]
        
    #     writer = csv.DictWriter(ft_ds_ref, fieldnames=fields)
    #     # Write the header row (column names)
    #     writer.writeheader()
    #     for paper in data_csv:
    #         writer.writerow(paper)
    
    # data_csv = []
    # print("Search in references started")
    # for paper in tqdm(papers_pdf_path):
    #     paper_name = paper.split("/")[-1].removesuffix("PDF")
    #     #Get the abstract part
    #     search_res = search_dataset_in_section(paper,"references",ds_info,"title")
    #     search_res["name"] = paper_name
    #     data_csv.append(search_res)
            
    # with open("./Results/extraction/fulltext_datasets_references.csv","w",newline="") as ft_ds_ref:
    #     fields = ["name"]
    #     fields += [ds_name for ds_name in ds_info]
        
    #     writer = csv.DictWriter(ft_ds_ref, fieldnames=fields)
    #     # Write the header row (column names)
    #     writer.writeheader()
    #     for paper in data_csv:
    #         writer.writerow(paper)
    
    # data_csv = []
    # print("Search in results started")
    # for paper in tqdm(papers_pdf_path):
    #     paper_name = paper.split("/")[-1].removesuffix("PDF")
    #     #Get the abstract part
    #     search_res = search_dataset_in_section(paper,"results",ds_info)
    #     search_res["name"] = paper_name
    #     data_csv.append(search_res)
            
    # with open("./Results/extraction/fulltext_datasets_results.csv","w",newline="") as ft_ds_ref:
    #     fields = ["name"]
    #     fields += [ds_name for ds_name in ds_info]
        
    #     writer = csv.DictWriter(ft_ds_ref, fieldnames=fields)
    #     # Write the header row (column names)
    #     writer.writeheader()
    #     for paper in data_csv:
    #         writer.writerow(paper)

    # data_csv = []
    # print("Search in method started")
    # for paper in tqdm(papers_pdf_path):
    #     paper_name = paper.split("/")[-1].removesuffix("PDF")
    #     #Get the abstract part
    #     search_res = search_dataset_in_section(paper,"method",ds_info)
    #     search_res["name"] = paper_name
    #     data_csv.append(search_res)
            
    # with open("./Results/extraction/fulltext_datasets_method.csv","w",newline="") as ft_ds_ref:
    #     fields = ["name"]
    #     fields += [ds_name for ds_name in ds_info]
        
    #     writer = csv.DictWriter(ft_ds_ref, fieldnames=fields)
    #     # Write the header row (column names)
    #     writer.writeheader()
    #     for paper in data_csv:
    #         writer.writerow(paper)

if __name__ == "__main__":
    main()