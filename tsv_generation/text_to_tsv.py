import sys
import json
import csv
from os import listdir
from os.path import isfile, join
import pandas as pd
from pandas.io.json import json_normalize

entity_1 = 'gene'
entity_2 = 'disease'
mypath = '../comm_use_subset_100/'  #TODO: Probably better to use 'sys' so that path can be specified by user
meta_data = pd.read_csv('metadata_comm_use_subset_100.csv')


for sha in meta_data['sha']:
    with open(mypath + sha + '.json', 'r') as json_file:
        with
        data = json.load(json_file) #Dictionary containing the json file
        nycphil = json_normalize(data)
        print(nycphil)
     
       
