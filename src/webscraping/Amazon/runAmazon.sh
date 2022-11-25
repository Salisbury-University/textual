#!/bin/bash 

cd reviews

for file in *; do
	echo $file
	python3.8 ../readAmazon.py /root/textual/src/webscraping/Amazon/reviews/$file
done
