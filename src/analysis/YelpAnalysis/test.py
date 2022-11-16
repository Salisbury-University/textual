import glob
import re

file_list = (glob.glob("train_dataset/*/*.txt"))

for input_file in file_list:
    new_file = open(input_file)
    text = new_file.read()

    rating = input_file
    rating = re.sub("train_dataset/star_", "", rating)
    rating = re.sub("/.*", "", rating)

    print(text + " " + rating)
