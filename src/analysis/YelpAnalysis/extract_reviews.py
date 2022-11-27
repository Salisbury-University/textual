import json
import pandas as pd

data = pd.DataFrame()

i=0

with open("reviews.json") as input_file: 
    for line in input_file:
        if i % 10000 == 0:
            print(i)
        
        i = i + 1

        json_obj = json.loads(line)
        data = data.append({"stars" : json_obj["stars"], "text" : json_obj["text"]}, ignore_index=True)

data.to_csv("reviews.csv", index=False)
