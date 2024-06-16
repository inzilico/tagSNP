"""
Functions to assista the data processing.
Author: Gennady Khvorykh, info@inzilico,com
"""

import os
import sys

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
