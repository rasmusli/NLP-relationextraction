import sys
import json
import csv
import os
import pandas as pd
from os.path import isfile, join
from collections import OrderedDict
from operator import getitem


"""
This script reads a folder of PUBAnnotated json files (dir_path)
to convert to test.tsv file with tokens ready for Relation extraction.

The obj in the pubannotations needs to be correctly named according to 
Relation extraction tokens (gene, desease etc.) or it needs to be taken care of in the get_text_with_token-function
"""
def find_all(scentence, string, start, end): # Not used any more
    """
    Recursively finds indeces of all instances if a string in a sentence
    """
    start = sentence.find(string, start, end)
    if start == -1:
        return []
    else:
        return [start] + find_all(sentence, string, start+1, len(sentence))

def get_text_with_token(json_file):
    data = json.load(json_file)
    denotations = data['denotations']
    den_sorted =  sorted(denotations, key = lambda i: i['span']['begin'])
    original_text = data['text']
    replaced_words = list()
    for denotation in reversed(den_sorted):    #Reversed so changes dont 
        start = denotation['span']['begin']     #Start index of entity
        end = denotation['span']['end']         #End index of entity
        denot = {}
        denot['begin'] = start
        denot['end'] = end
        denot['word'] = data['text'][start:end]
        denot['mask'] = '@' + denotation['obj'].upper() + '$'
        denot['denot'] = denotation
        replaced_words.append(denot)
        #print(denot)
        data['text'] = data['text'][:start] + '@' + denotation['obj'].upper() + '$ ' + data['text'][end:]   #replace entity with @"obj"$
    return data['text'].split(' . '), original_text, replaced_words

dir_path = 'gene_disease_combined/'
entity1 = "@GENE$"
entity2 = "@DISEASE$"
#dir_path = '../output_generation/test_folder/'

with open('gene_disease.tsv', 'w') as out_file:
    with open('sentence_locations.tsv', 'w') as out_file_analysis:
        index = 0
        out_file.write('index\tsentence\tlabel\n')      #First row of test.tsv file
        out_file_analysis.write('index\tmasked sentence\toriginal sentence\tjson file\tsentence begin\tsentence end\tdenotation 1\tdenotation 2\n')
        for json_file_name in os.listdir(dir_path):     #Loop through all json files in directory
            with open(dir_path + json_file_name) as json_file:
                sentences, original_text, replaced_words = get_text_with_token(json_file) #split on " . " to divide running text into sentences
                original_scentences = original_text.split(' . ')
                i = 0
                for masked_sentence in sentences:
                    if entity1 in masked_sentence and entity2 in masked_sentence:
                        print('Sentence: ')
                        print(masked_sentence)
                        entity1_words = list()
                        entity2_words = list()
                        sentence_start = original_text.find(original_scentences[i])
                        sentence_end = original_text.find(original_scentences[i])+ len(original_scentences[i])
                        for word in replaced_words:
                            if word['begin'] > sentence_start and word['end'] < sentence_end:
                                if word['mask'] == entity1:
                                    entity1_words.append(word)
                                else:
                                    entity2_words.append(word)

                        for word_e1 in entity1_words:
                            for word_e2 in entity2_words:
                                if word_e1['begin'] < word_e2['begin']:
                                    mask_begin_e1 = original_scentences[i].find(word_e1['word'])
                                    mask_end_e1 = original_scentences[i].find(word_e1['word']) + len(word_e1['word'])
                                    mask_begin_e2 = original_scentences[i].find(word_e2['word'])
                                    mask_end_e2 = original_scentences[i].find(word_e2['word']) + len(word_e2['word'])
                                    sentence = original_scentences[i][:mask_begin_e1] + word_e1['mask'] + original_scentences[i][mask_end_e1-1:mask_begin_e2] + word_e2['mask'] + original_scentences[i][mask_end_e2-1:]
                                    out_file.write(str(str(index) + '\t' + sentence + '\t' + '1\n')) #write to file according to format of test.tsv for RE
                                    out_file_analysis.write(str(index) + '\t' + sentence + '\t' + original_scentences[i] + '\t' +json_file_name+ '\t' +str(sentence_start)+ '\t' +str(sentence_end)+ '\t' +str(word_e1['denot'])+ '\t' +str(word_e2['denot'])+ '\n')
                                    index += 1  #increase index for each row/sentence sentence
                                else:
                                    mask_begin_e1 = original_scentences[i].find(word_e1['word'])
                                    mask_end_e1 = original_scentences[i].find(word_e1['word']) + len(word_e1['word'])
                                    mask_begin_e2 = original_scentences[i].find(word_e2['word'])
                                    mask_end_e2 = original_scentences[i].find(word_e2['word']) + len(word_e2['word'])
                                    sentence = original_scentences[i][:mask_begin_e2] + word_e2['mask'] + original_scentences[i][mask_end_e2-1:mask_begin_e1] + word_e1['mask'] + original_scentences[i][mask_end_e1-1:]
                                    out_file.write(str(str(index) + '\t' + sentence + '\t' + '1\n')) #write to file according to format of test.tsv for RE
                                    index += 1  #increase index for each row/sentence sentence
                        
                    i += 1
    out_file_analysis.close()
out_file.close()
