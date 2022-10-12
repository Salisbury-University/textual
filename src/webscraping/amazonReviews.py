import json
import sys

SOURCE_FILE=sys.argv[1]

def open_file():
    print(SOURCE_FILE)
    #with open(SOURCE_FILE) as json_file:
    #    data = json.load(json_file)
    #    return data
    f = open(SOURCE_FILE,)
    data = json.load(f)
    return data

if __name__ =="__main__":
    data = open_file
    print(data)
