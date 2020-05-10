import sys
import json
import csv
import os
from os import listdir
from os.path import isfile, join

"""
This script combines pub_annot files with different entities into one. It is done by reading from two
different folders that are containing the same files and outputing a new folder with the combined entities.
"""

folder_1 = 'gene' #First folder to read from
folder_2 = 'disease' #Second folder to read from
output_dir = 'test_dir' #Output folder name, the script will create one if one does not already exist
try:
    os.mkdir(output_dir)
except:
    pass

for file in listdir(entity_1): #Read all files in first folder (folder 1 and 2 should contain same file-names)
    with open(folder_1 + '/' + file , 'r') as json_1: #Open pub-annot files of entity 1
        with open(folder_2 + '/' + file , 'r') as json_2: #Open pub-annot files of entity 2

            data_1 = json.load(json_1) #Dictionary containing the json file
            data_2 = json.load(json_2)
            ID = len(data_1['denotations']) #Start value when appending new denotations

            for denot in data_2['denotations']: #Loop for all denotations in file 2 to add to file 1
                ID += 1
                denot['id'] = ID #Change the ID to fit in file 1
                data_1['denotations'].append(denot) #Append the denotation to file 1

            with open(output_dir+'/' + file , 'w') as out_file:
                out_file.write(json.dumps(data_1))
