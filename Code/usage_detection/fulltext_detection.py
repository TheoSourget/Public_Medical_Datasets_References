import pdf_utilities.pdf_utilities as pdf_util
import glob
import csv
import re

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
                                         }
    return datasets_info


def search_dataset_in_section(paper_path,section_name,dataset_infos):
    res = {ds_name:False for ds_name in dataset_infos}
    text = pdf_util.extract_section(paper_path,section_name)
    if text:
        text = " ".join(text)
        for ds_name in dataset_infos:
            if re.search(f"(?<![^_\\W]){ds_name}(?![^_\\s\\d\\.])",text):
                res[ds_name] = True
            else:
                for alias in dataset_infos[ds_name]["aliases"]:
                    if re.search(f"(?<![^_\\W]){alias}(?![^_\\s\\d\\.])",text):
                        res[ds_name] = True
                        break
    return res
def main():
    #Load dataset_info
    ds_info = load_datasets_info()

    #Load list of downloaded pdf 
    papers_pdf_path = glob.glob("./Results/extraction/fulltext/*.PDF")
    data_csv = []
    for paper in papers_pdf_path:
        paper_name = paper.split("/")[-1].removesuffix("PDF")
        #Get the abstract part
        search_res = search_dataset_in_section(paper,"abstract",ds_info)
        search_res["name"] = paper_name
        data_csv.append(search_res)
    
    with open("./Results/extraction/fulltext_datasets_abstract.csv","w",newline="") as ft_ds_ref:
        fields = ["name"]
        fields += [ds_name for ds_name in ds_info]
        
        writer = csv.DictWriter(ft_ds_ref, fieldnames=fields)
        # Write the header row (column names)
        writer.writeheader()
        for paper in data_csv:
            writer.writerow(paper)
    
    data_csv = []
    for paper in papers_pdf_path:
        paper_name = paper.split("/")[-1].removesuffix("PDF")
        #Get the abstract part
        search_res = search_dataset_in_section(paper,"references",ds_info)
        search_res["name"] = paper_name
        data_csv.append(search_res)
            
    with open("./Results/extraction/fulltext_datasets_references.csv","w",newline="") as ft_ds_ref:
        fields = ["name"]
        fields += [ds_name for ds_name in ds_info]
        
        writer = csv.DictWriter(ft_ds_ref, fieldnames=fields)
        # Write the header row (column names)
        writer.writeheader()
        for paper in data_csv:
            writer.writerow(paper)
    
    data_csv = []
    for paper in papers_pdf_path:
        paper_name = paper.split("/")[-1].removesuffix("PDF")
        #Get the abstract part
        search_res = search_dataset_in_section(paper,"results",ds_info)
        search_res["name"] = paper_name
        data_csv.append(search_res)
            
    with open("./Results/extraction/fulltext_datasets_results.csv","w",newline="") as ft_ds_ref:
        fields = ["name"]
        fields += [ds_name for ds_name in ds_info]
        
        writer = csv.DictWriter(ft_ds_ref, fieldnames=fields)
        # Write the header row (column names)
        writer.writeheader()
        for paper in data_csv:
            writer.writerow(paper)

if __name__ == "__main__":
    main()