from grobid_client.grobid_client import GrobidClient
import glob
import shutil
import os
if __name__ == "__main__":
    fulltext_pdfs= glob.glob("./Results/extraction/fulltext/*.pdf")
    already_converted = [f.removesuffix(".grobid.tei.xml").removeprefix("./Results/extraction/grobid_extraction/") for f in glob.glob("./Results/extraction/grobid_extraction/*.xml")]

    #Clean pdf folder
    for f in glob.glob("./Code/grobid/to_convert/*.pdf"):
        os.remove(f)
    
    #Get the pdfs to convert
    for p in fulltext_pdfs:
        doc_name = p.removesuffix(".pdf").removeprefix("./Results/extraction/fulltext/")
        if doc_name not in already_converted:
            shutil.copy(p,f"./Code/grobid/to_convert/{doc_name}.pdf")
    client = GrobidClient(config_path="./Code/grobid/grobid_client_python/config.json")
    client.process("processFulltextDocument", "./Code/grobid/to_convert/","./Results/extraction/grobid_extraction/", consolidate_citations=True, tei_coordinates=True,force=True)
    
    #Clean pdf folder
    for f in glob.glob("./Code/grobid/to_convert/*.pdf"):
        os.remove(f)

    #Remove failed convertion (result in .txt files) 
    # for f in glob.glob("./Results/extraction/grobid_extraction/*.txt"):
    #     os.remove(f)