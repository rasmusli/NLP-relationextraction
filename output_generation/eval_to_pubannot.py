##This script transforms the output file given by BioBERT and outputs a JSON files
#in the PubAnnotation format. It requires the file 'rebuild_reference.txt' to do so.
# This file is generated by the 'json_to_txt.py' script in the dataset_generation folder.

import re
import json

def extract_text_entities(raw_parag):
    # Function that obtains the full text, the entities and their positions
    # form a paragraph in the '<word> <tag> <tag>' format outputed by BioBERT

    full_parag = ''  # Full text of the paragraph
    entities = []  # List of entities
    ent_positions = []  # List of tuples containing the positions of the entities

    single_entity = ''
    for line in raw_parag:
        # Rebuild text from the tsv file
        word = re.findall(r'^([\S]+)',line)[0] #Isolate the word
        full_parag = full_parag + word + ' '  # Add the word to the full text
        #TODO: The space makes special characters to be separated. Could be fixed.

        # Isolate Named Entites using info from the tsv file
        if re.findall(r'B-MISC',line): #TODO: THIS CODE IS REALLY FRAGILE. FIX!
            single_entity = word
            start_pos = len(full_parag) - len(word) - 1 #-1 because 1st pos is 0
        elif re.findall(r'I-MISC',line) and single_entity != '':
            single_entity = single_entity + ' ' + word
        else:
            if single_entity != '':  # If the variable 'single_entity' had an entity stored, store it.
                entities.append(single_entity)
                end_pos = len(full_parag) - len(word) - 1
                ent_positions.append((start_pos, end_pos))
            single_entity = ''

    if single_entity != '': #In case last word in the paragraph is a 'B'
            entities.append(single_entity)
            end_pos = len(full_parag)-1
            ent_positions.append((start_pos, end_pos))

    return full_parag.rstrip(), entities, ent_positions
#TODO: Apparently regex matches can give you start-end indexes. So it might be better to use that!

f = open('../dataset_generation/rebuild_reference.txt', 'r')
lines = f.readlines()  # Open the reference file, which contains the names of the output filenames
# This is necessary because the BioBERT output file has no info of ID or text type (title, abstract...)

with open('./NER_result_conll.txt', 'r') as in_file:
    paragraph = []
    #count = 0  # Counter for testing purposes. DELETE LATER
    par_counter = 0
    for line in in_file:
        if line == '\n':  # End of paragraph
            metadata = lines[par_counter].split()  # EXTRACT TITLE FROM REFERENCE FILE
            par_counter += 1
            title = metadata[0]
            with open('pubanot_jasons/' + title + '.json', 'w') as out_file:
                full_text, ents, ent_span = extract_text_entities(paragraph)
                denot_array = []
                if ents: #If there are entities for this paragraph
                    for i in range(len(ents)):
                        denot_array.append({"id": i+1, "span": {"begin": ent_span[i][0], "end": ent_span[i][1]}, "obj": 'ne'})
                tmp_dict = {
                    "cord_uid": metadata[1], # first 4 can be found in 'lines' !
                    "sourcedb": metadata[2],
                    "sourceid": metadata[3],
                    "divid": metadata[4],
                    "text": full_text, #Add full text
                    "project": "cdlai_CORD-19", # A fixed expression defined by us
                    "denotations": denot_array  # Add all entities
                }
                out_file.write(json.dumps(tmp_dict))
            paragraph = [] #Empty paragraph
            #count += 1 #Counter for testing purposes. DELETE LATER
            #if count > 2: #Counter for testing purposes. DELETE LATER
            #    break #Counter for testing purposes. DELETE LATER
        else:
            paragraph.append(line)