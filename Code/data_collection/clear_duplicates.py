import glob
import os

if __name__ == "__main__":
    nb_problem = 0
    files = glob.glob("./Results/extraction/fulltext/*..pdf")
    files_without_extension = [fname.removesuffix(".pdf") for fname in files]
    files_without_extension = [fname.removesuffix(".") for fname in files_without_extension]
    for f in files_without_extension:
        if len(glob.glob(f"{f}*")) > 1:
            nb_problem += 1
            os.remove(f"{f}..pdf")
    print(nb_problem)
