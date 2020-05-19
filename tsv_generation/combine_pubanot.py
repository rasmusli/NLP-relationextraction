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

folder_1 = 'JNLPBA_PubAnno' #First folder to read from
folder_2 = 'JNLPBA_PubAnno' #Second folder to read from
output_dir = 'gene_disease_combined_test' #Output folder name, the script will create one if one does not already exist
try:
    os.mkdir(output_dir)
except:
    pass

for file in listdir(folder_1): #Read all files in first folder (folder 1 and 2 should contain same file-names)
    with open(folder_1 + '/' + file , 'r') as json_1: #Open pub-annot files of entity 1
        with open(folder_2 + '/' + file , 'r') as json_2: #Open pub-annot files of entity 2

            data_1 = json.load(json_1) #Dictionary containing the json file
            data_2 = json.load(json_2)

            for denot in data_2['denotations']: #Loop for all denotations in file 2 to add to file 1
                data_1['denotations'].append(denot) #Append the denotation to file 1

            # Next we need to remove overlapping denotations, keeping the longest denotation
            new_denotations = [] #Create new denotation list
            ID = 1 # With 'id' staring at 1

            denotations = data_1['denotations'] #Extract denotations
            den_sorted =  sorted(denotations, key = lambda i: i['span']['begin']) #Sort on begin of the span
            
            index = 0
            while(index<len(den_sorted)-2): #Outer loop to walk through all denotation
                
                #Delete denotations that are overlapping, keep the longest one
                longest_denot = den_sorted[index]
                longest_length = longest_denot['span']['end'] - longest_denot['span']['begin']
                
                for k in range(index+1, len(den_sorted)): #Inner loop to to check forward denotations for overlap
                    denot = den_sorted[k]

                    if denot['span']['begin'] < longest_denot['span']['end']: #Means we have overlap
                        length = denot['span']['end'] - denot['span']['begin'] 
                        if length > longest_length: #Keep the longest one
                            longest_denot = denot
                            longest_length = length
                    else:
                        longest_denot['id'] = ID #Set new ID for the denotation
                        new_denotations.append(longest_denot) #Append to the new denotation list
                        ID += 1 
                        index = k #Jump over the already checked denotations
                        break #No need to check the rest of the list since it is sorted
                break #If we reach here means we checked all denotations for overlap

                    

            data_1['denotations'] = new_denotations
            with open(output_dir+'/' + file , 'w') as out_file:
                out_file.write(json.dumps(data_1))
