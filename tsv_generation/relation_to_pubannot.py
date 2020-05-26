import re
import json
import pandas as pd

def create_relation(ref_line, ID):
    relation = {}
    relation["id"] = ID
    str_1 = ref_line['denotation 1']
    str_2 = ref_line['denotation 2']
    str_1 = str_1.replace("\'", "\"")
    str_2 = str_2.replace("\'", "\"")
    den_1 = json.loads(str_1)
    den_2 = json.loads(str_2)
    relation["subj"] = den_1['id']
    relation["obj"] = den_2['id']
    relation["pred"] = "interactWith"
    return relation

def thresh_hold(probability):
    return 1 if probability > 0.5 else 0

pred_path = "../subset_predictions/gad_predictions.xlsx" #The predictions from BioBERT, indexes needs to match reference file
reference_file = "../dataset_generation/sentence_locations.tsv" #Reference file that contains information about location of sentences
pub_annot_folder = "gene_disease_combined" #NOTE: the script will write in the existing folder files, so files will be overwritten

xls = pd.ExcelFile(pred_path)
prediction = pd.read_excel(xls, 'Intersection',index_col=0)
reference = pd.read_csv(reference_file, delimiter='\t',header=0)

for i in range(len(reference)): #Loop through all sentences that has a class1 and class2
    ref_line = reference.loc[i] #Check
    if prediction.iloc[i,0]:
        with open(pub_annot_folder + '/' + ref_line['json file'],'r') as json_file: #Open pubannot file
            data = json.load(json_file)
            try:
                relations = data['relations']
                ID = len(relations)+1
            except:
                relations = []
                ID = 1

            rel = create_relation(ref_line, ID)
            relations.append(rel)

            data['relations'] = relations

            with open(pub_annot_folder+'/'+ref_line['json file'],'w') as out_file:
                out_file.write(json.dumps(data))

#Only used to generate file to sonja to evaluate predictions
"""
true_predictions = pd.DataFrame()
count = 0
for i in range(len(reference)):
    ref_line = reference.loc[i]
    if prediction.iloc[i,0]:
        true_predictions[count] = ref_line
        count += 1

true_predictions = true_predictions.transpose()
writer = pd.ExcelWriter("../subset_predictions/sonjas_evaluation_file_union.xlsx")
true_predictions.to_excel(writer,'Sheet 1')
writer.save()
"""