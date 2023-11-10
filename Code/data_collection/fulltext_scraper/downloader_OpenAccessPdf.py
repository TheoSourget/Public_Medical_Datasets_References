import requests
import pandas as pd
import csv
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import os
import glob

def main():
    downloaded_papers = glob.glob("./Results/extraction/fulltext/*.pdf")
    papers_info = pd.read_csv("./Results/extraction/papers_infos_openalex.csv")
    papers_info = papers_info.dropna(subset=["fulltext_link"])
    base_path = "./Results/extraction/fulltext/"
    for title,paper_url in zip(papers_info["title"],papers_info["fulltext_link"]):
        file_path = f"{base_path}{title.replace('/',' ')}.pdf"
        if file_path not in downloaded_papers:
            try:
                r_fulltext = requests.get(paper_url,allow_redirects=True,timeout=10)
                pdf_content = r_fulltext.content
                if r_fulltext.status_code == 200:
                    open(file_path,"wb").write(r_fulltext.content)
                    try:
                        #Try to read the pdf (Raise an error if the file is an invalid pdf)
                        PdfReader(file_path,strict=True)
                    except PdfReadError:
                        #If a PdfReadError is raised, the pdf is invalid and therefore removed from downloaded list
                        os.remove(file_path) 
                else:
                    continue
            except requests.exceptions.RequestException as ce:
                continue
            
if __name__ == "__main__":
    main()