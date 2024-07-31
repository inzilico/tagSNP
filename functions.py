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
    
    # Create dataframe
    #df = pd.DataFrame({"chrom": chrom, "pos": pos, "rs": rs})
    return(out)
    
    