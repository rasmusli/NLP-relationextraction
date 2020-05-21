import re
import json
import pandas as pd

def create_relation(ref_line, ID):
    relation = {}
    relation["id"] = ID
    relation["subj"] = ref_line['denotation 1']
    relation["obj"] = ref_line['denotation 2']
    relation["pred"] = "interactWith"

def thresh_hold(probability):
    return 1 if probability > 0.5 else 0

pred_path = "../subset_predictions/gad_predictions.xlsx"
pub_annot_folder = "gene_disease_combined"
reference_file = "sentence_locations.tsv"

xls = pd.ExcelFile(pred_path)
prediction = pd.read_excel(xls, 'Intersection',index_col=0)
print(prediction)
reference = pd.read_csv(reference_file, delimiter='\t',header=0)
print(reference)

for i in range(len(reference)):
    ref_line = reference.iloc[i]
    with open(pub_annot_folder + '/' + ref_line['json file']) as json:
        data = json.load(json)
        if prediction.iloc[0]:
            try:
                relations = data['relations']
                ID = len(relations)
            except:
                relations = []
                ID = 1

            rel = create_relation(ref_line, ID)
            relations.append(rel)

        with open(pub_annot_folder+'/'+ref_line['json file']) as outfile:
            out_file.write(json.dumps(data))
    
    
