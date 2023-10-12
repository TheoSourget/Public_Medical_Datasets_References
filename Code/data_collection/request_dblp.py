"""
This script gather the list of papers from venues in the Resources/data/venues.csv.
The result will be a csv file in Results/extraction/papers_from_venues.csv 

Usage:
From root directory:
    python request_dblp.py
"""
import requests
import csv

def gather_for_venue(venue_name,api_link,start_year,end_year):
    """
    Query dblp api with api_link parameter to search gather papers from the venue specified in venue_name between start_year and end_year.
    @params:
        -venue_name (string): Name of the venue (ex: "MICCAI" or "MIDL")
        -api_link (string): dblp api link for the specific venue
        -start_year (int): minimal publication year for the paper to be kept (include)
        -end_year (int): maximal publication year for the paper to be kept (include)
    @return:
        A list of dictionary, each element containing the following fields: doi,title,venue 
    """
    indice_paper = 0
    nextPage = True
    #Dictionnary with doi as key and title as value
    lst_paper = []
    while nextPage:
        # Construct the url adding the index of the first paper (useful to parse multiple page)
        request_url = f"{api_link}&f={indice_paper}"      
        request = requests.get(request_url)
        if request.status_code == 200:
            r_json = request.json()
            if r_json["result"]["hits"]["@sent"] != '0':
                for paper in r_json["result"]["hits"]["hit"]:
                    if ("doi" not in paper["info"] and "title" not in paper["info"]) or int(paper["info"]["year"]) <= start_year  or int(paper["info"]["year"]) >= end_year or paper["info"]["venue"] != venue_name:
                        continue
                    
                    title = paper["info"].get("title","None")
                    title = title.replace(",","")
                    title = title.replace("\n","")
                    year = paper["info"].get("year","None")
                    venue = paper["info"].get("venue","None")
                    doi = paper["info"].get("doi","None")
                    lst_paper.append({
                        "doi":doi,
                        "title":title,
                        "venue":venue
                    })
                indice_paper += 1000
            else:
                nextPage = False
    return lst_paper

def main():
    reader = csv.DictReader(open('./Resources/data/venues.csv'))
    #For each venue, gather the list of paper
    lst_papers_all = []
    for venue in reader:
        print("Current query:",venue["name"],venue["api_link"],int(venue["start_year"]),int(venue["end_year"]))
        lst_papers_venue = gather_for_venue(venue["name"],venue["api_link"],int(venue["start_year"]),int(venue["end_year"]))
        lst_papers_all += lst_papers_venue
    
    #Save the results in papers_from_venues.csv
    fields = ["doi", "title", "venue"]
    with open("./Results/extraction/papers_from_venues.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        # Write the header row (column names)
        writer.writeheader()
        
        # Write the data
        for paper in lst_papers_all:
            writer.writerow(paper)
    
    return lst_papers_all


if __name__ == "__main__":
    print("Extraction started")
    main()
    print("Extraction finished, see results at Results/extraction/papers_from_venues.csv")