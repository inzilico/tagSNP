"""
Functions to assista the data processing.
Author: Gennady Khvorykh, info@inzilico,com
"""

import os
import sys
import time
import numpy as np
import pandas as pd

def check_files(files: list):
    for file in files:
       if not os.path.isfile(file):
           print(file, "doesn't exist!")
           sys.exit(1) 

def load_resources(x: str):
    out = dict()
    with open(x, "r") as f:
        for line in f:
            arr = line.strip().split(",")
            out[arr[0]] = arr[1]
    return(out)

def time_elepsed(t):
    """ 
    Show time elapsed since time in argument
    """
    dur = time.time()-t
    dur = time.strftime("%H:%M:%S", time.gmtime(dur))
    print("Time spent: ", dur)
    
def subset_matrix(m, indexes):
    ind = [x - 1 for x in indexes]
    sm = [x[ind] for x in m[ind]]
    return(np.asmatrix(sm))

def bonacich_centrality(A):
    # Get dot product
    centrality = np.dot(A,A)
    # Calculate the sum of the elements in each row  
    row_sum = np.sum(centrality, axis=1)
    # Normalize 
    total_of_row = sum(row_sum)
    row_sum_normalized = row_sum/total_of_row
    # Convert matrix to list
    out = [i[0] for i in row_sum_normalized.tolist()]
    # Return 
    return(out)

def code_genotypes(x: str):
    out = []
    # Initiate variables
    with open(x, "r") as f:
        for line in f:
            if line.startswith("#"): continue
            line = line.strip()
            ar = line.split("\t")
            # Get ref and alt alleles
            al = ar[3:5]
            # Define minor allele
            vec = []
            gt = ar[9:]
            for x in gt:
                for y in x.split("|"):
                    vec.append(int(y))
            freq = sum(vec)/len(vec)             
            if (freq <= 0.5):
                minor = al[1]
                major = al[0]
                maf = freq
            else:
                minor = al[0]
                major = al[1]
                maf = 1 - freq
            # Code genotypes
            coded = []
            for x in gt:
                if x == "0|1" or x == "1|0":
                    coded.append(0)
                if x == "0|0" and minor == al[0]:
                    coded.append(-1)
                if x == "0|0" and minor == al[1]:
                    coded.append(1)
                if x == "1|1" and minor == al[0]:
                    coded.append(1)
                if x == "1|1" and minor == al[1]:
                    coded.append(-1)    
            out.append([ar[2], ar[1], f'{major}/{minor}', ",".join([str(x) for x in coded]), maf])
    
    return(out)


def restore_haplotypes(x: pd.Series, alleles):
    h1, h2 = [], []
    for i, gt in enumerate(x):
        minor, major = alleles[i]
        a1, a2 = gt.split("|")
        a1 = int(a1)
        a2 = int(a2)
        if a1 == minor: h1.append("1")
        if a1 == major: h1.append("0")
        if a2 == minor: h2.append("1")
        if a2 == major: h2.append("0")    
    return("|".join([" ".join(h1), " ".join(h2)]))
    #return(pd.DataFrame({"h1": h1, "h2": h2}))
    #return(" ".join(h1))
 
    
def get_haplotypes(vcf_file: str):
    
    # Create list of tuples with minor, major alleles
    alleles = []
    n = 0
    with open(vcf_file, "r") as f:
        for line in f:
            if line.startswith("#"): 
                n += 1
                continue
            line = line.strip()
            # Get fields
            ar = line.split("\t")
            # Subset genotypes
            gt = ar[9:]
            # Define minor/major allele
            vec = []
            for x in gt:
                for y in x.split("|"):
                    vec.append(int(y))
            freq = sum(vec)/len(vec)             
            if (freq <= 0.5):
                minor = 1
                major = 0
            else:
                minor = 0
                major = 1
            # Update variants
            alleles.append((minor, major))
    print("No of SNPs:", len(alleles))
    # Load genotypes
    df = pd.read_csv(vcf_file, sep="\t", header=None, skiprows=n).iloc[:, 9:]
    # Restore haplotypes
    res = df.apply(restore_haplotypes, axis="index", raw=True, alleles=alleles)
    res = res.str.split(pat="|", expand=True)
    return(res.stack())
    