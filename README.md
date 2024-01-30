# Citation Needed
This project aims at the quantification of dataset usage in scientific papers. 
The code works as displayed in the following figure:

![](./Resources/images/flowchart_logo.png)

# Input data
Before starting the different scipts, two files must be filled with information for the venues (venues.csv) and the datasets (datasets.csv).

# Process
The process is divided in 3 parts:

The list of papers from the venues is obtained using the DBLP API. 

Then, the paper DOI (or title if the DOI is not available) is used to query the OpenAlex API to get the following: (i) list of 
referenced papers, (ii) list of words in the abstract, and (iii) open access link to the paper's full text.
The full-text is then fetch using the link from OpenAlex or a custom tool can be added to the process.

The PDF are then convert using GROBID, regex matching are done to detect mentions while matching of OpenAlex ID and regex are used to gather the citations. 

Finally, a notebook provides code to make some figures about the type of presence or the number of citations/mention for a dataset.

# Install & Usage
Soon
