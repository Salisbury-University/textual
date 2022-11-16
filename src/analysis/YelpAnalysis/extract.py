import sys 
import json
import multiprocessing as mp
import threading
import functools as ft
import numpy as np

# Extract data and save in file
def extract_text(input_data):
    i = 0
    
    for json_obj in input_data:
        text = json_obj["text"]
               
        # Open file for current interation
        output_file = open("./train/5_star/textdata_" + str(mp.current_process()._identity) + "_" + str(i) + ".txt", "w")
        # Write data
        output_file.write(text)
        output_file.close()
        
        if i % 1000 == 0:
            print("Iteration: "+ str(i) + " on thread " + str(mp.current_process()._identity))

        # Increment index
        i = i + 1


    # Main
if __name__ =="__main__":
    line_list = []

    with open(sys.argv[1]) as input_file:
        for line in input_file:
            json_obj = json.loads(line)
            
            #Append line to list
            line_list.append(json_obj)
    # Close file
    input_file.close()

    reviewArray = np.array_split(line_list, mp.cpu_count())

    # Create pool
    pool=mp.Pool(mp.cpu_count())

    pool.map(extract_text, [sublist for sublist in reviewArray])
            
    pool.close()


