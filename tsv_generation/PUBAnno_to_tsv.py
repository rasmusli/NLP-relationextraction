import sys
import json
import csv
import os
from os.path import isfile, join

mypath = '../comm_use_subset_100/'

def get_text_with_token(json_file):
    data = json.load(json_file)
    for denotation in reversed(data['denotations']):
        start = denotation['span']['begin']
        end = denotation['span']['end']
        print(start)
        print(end)
        data['text'] = data['text'][:start] + '@' + denotation['obj'].upper() + '$ ' + data['text'][end:]
    return data['text']


dir_path = '../output_generation/test_folder/'

with open('../output_generation/test_folder/generated_test.tsv', 'w') as out_file:
    index = 0
    out_file.write('index\tsentence\tlabel\n')
    for json_file_name in os.listdir(dir_path):
        with open(dir_path + json_file_name) as json_file:
            sentences = get_text_with_token(json_file).split(' . ')
            for sentence in sentences:
                out_file.write(str(index) + '\t' + sentence + '\t' + '1\n')
                index += 1




"""
with open('generated_test.tsv', 'w') as out_file:
    with open(../ + 'meta_subset_100.csv') as meta_data_file:
"""
