"""
Functions to assista the data processing.
Author: Gennady Khvorykh, info@inzilico,com
"""

import os
import sys
import time
import numpy as np

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