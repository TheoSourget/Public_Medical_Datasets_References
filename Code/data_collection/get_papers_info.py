"""
This script get information of papers in Resources/data/venues.csv (obtained with request_dblp.py) using openalex API.
The result will be a csv file in Results/extraction/papers_infos_openalex.csv 

Usage:
From root directory:
    python get_papers_info.py
"""
import requests
import csv
from tqdm import tqdm

def query_openalex_by_title(title,venue):
    """
    Query OpenAlex API with the title of the paper in case the doi is unknown.
    @param:
        -title: title of the paper to search for
        -venue: name of the venue the paper was published in (useful for saving and futur usage)
    @return:
        -dictionary with the paper information if found on openalex, None otherwise
    """

    request_url = f'https://api.openalex.org/works?search="{title}"'
    request = requests.get(request_url)
    if request.status_code == 200:
        query_json = request.json()

        if query_json["meta"]["count"] == 0:
            paper_infos = {
                    "doi":"None",
                    "title":title,
                    "venue":venue,
                    "year":"None",
                    "abstract":"None",
                    "references":"None",
                    "fulltext_link":"None"
                }
            return paper_infos

        r_json = query_json["results"][0]
        fulltext_url = "None"
        if r_json.get("open_access",None):
            if r_json["open_access"].get("oa_url",None):
                fulltext_url = r_json["open_access"]["oa_url"]
            else:
                if r_json["primary_location"]:
                    if r_json["primary_location"]["pdf_url"]:
                        fulltext_url = r_json["primary_location"]["pdf_url"]
                    elif r_json["primary_location"]["landing_page_url"].endswith("pdf"):
                        fulltext_url = r_json["primary_location"]["landing_page_url"]
                    else:
                        fulltext_url = "None"
                else:
                    fulltext_url = "None"
        references = r_json['referenced_works']
        if len(references) == 0:
            references = "None"
        paper_infos = {
                "doi":"None",
                "title":title,
                "venue":venue,
                "year":r_json["publication_year"],
                "abstract":r_json["abstract_inverted_index"],
                "references":references,
                "fulltext_link":fulltext_url
            }
        return paper_infos
    return None

def query_openalex_by_doi(doi,venue):
    """
    Query OpenAlex API with the doi of the paper.
    @param:
        -doi: doi of the paper to search for
        -venue: name of the venue the paper was published in (useful for saving and futur usage)
    @return:
        -dictionary with the paper information if found on openalex, None otherwise
    """
    request_url = f"https://api.openalex.org/works/https://doi.org/{doi}"
    request = requests.get(request_url)
    if request.status_code == 200:
        r_json = request.json()
        if r_json["open_access"] and r_json["open_access"]["oa_url"]:
            fulltext_url = r_json["open_access"]["oa_url"]
        else:
            if r_json["primary_location"]:
                if r_json["primary_location"]["pdf_url"]:
                    fulltext_url = r_json["primary_location"]["pdf_url"]
                elif r_json["primary_location"]["landing_page_url"].endswith("pdf"):
                    fulltext_url = r_json["primary_location"]["landing_page_url"]
                else:
                    fulltext_url = "None"
            else:
                fulltext_url = "None"
                
        title = r_json["title"]
        title = title.replace(",","")
        title = title.replace("\n","")
        references = r_json['referenced_works']
        if len(references) == 0:
            references = "None"
        paper_infos = {
                "doi":doi,
                "title":title,
                "venue":venue,
                "year":r_json["publication_year"],
                "abstract":r_json["abstract_inverted_index"],
                "references":references,
                "fulltext_link":fulltext_url
            }
        return  paper_infos
    return None
   
def main():
    lst_doi = []
    lst_title = []
    
    #Get the list of papers already processed (useful to restart the process after an OpenAlex problem)
    try:
        with open("./Results/extraction/papers_infos_openalex.csv") as info_csv:
            reader = csv.DictReader(info_csv)
            for paper in reader:
                if paper["doi"] != "None":
                    lst_doi.append(paper["doi"])
                if paper["title"] != "None":
                    lst_title.append(paper["title"])
        file_exist = True
    except:
        file_exist = False
        pass
    
    
    nb_papers = sum(1 for row in open('./Results/extraction/papers_from_venues.csv'))-1 # -1 because of header
    reader = csv.DictReader(open('./Results/extraction/papers_from_venues.csv'))
    lst_papers_info = []
    
    with open("./Results/extraction/papers_infos_openalex.csv", "a", newline="") as csvfile:
        
        fields = ["doi", "title", "venue","year","abstract","references","fulltext_link"]
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        if not file_exist:
            # Write the header row (column names)
            writer.writeheader()
        
        for paper in tqdm(reader,total=nb_papers):
            
            if paper["doi"] in lst_doi or paper["title"] in lst_title:
                continue
            
            if paper["doi"] != "None":
                paper_info = query_openalex_by_doi(paper["doi"],paper["venue"])
            else:
                paper_info = query_openalex_by_title(paper["title"],paper["venue"])
            
            if paper_info:
                
                lst_papers_info.append(paper_info)
                writer.writerow(paper_info)

if __name__ == "__main__":
    print("Extraction started")
    main()
    print("Extraction finished, see results at Results/extraction/papers_infos_openalex.csv")