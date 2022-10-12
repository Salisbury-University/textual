import numpy as np
import json
import sys
import pandas as pd

SOURCE_FILE=sys.argv[1]

def open_file():
    print(SOURCE_FILE)
    df = pd.read_json(SOURCE_FILE)
    return df

if __name__ =="__main__":
    data = open_file
    display(data)
    #print(data)
