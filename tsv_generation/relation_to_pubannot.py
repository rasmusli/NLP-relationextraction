import re
import json
import pandas as pd

def create_relation(ref_line, ID):
    relation = {}
    relation["id"] = ID
    relation["subj"] = ref_line['denot1']
    relation["obj"] = ref_line['denot2']
    relation["pred"] = "interactWith"

def thresh_hold(probability):
    return 1 if probability > 0.5 else 0

pred_path = "../Results/test_results_gad_1_fine_tune.tsv"
pub_annot_folder = 
reference_file = ".."

predictions = pd.read_csv(pred_path,delimiter='\t',header=None)
predictions.columns = ['No Relations', 'Relations']

reference = pd.read_csv(pred_path,delimiter='\t',header=None)


for i in range(len(reference)):
    ref_line = reference.iloc[i]
    with open(pub_annot_folder + '/' + ref_line['json']) as json:
        data = json.load(json)
        if thresh_hold(predictions.loc[i,'Relations']):
            try:
                relations = data['relations']
                ID = len(relations)
            except:
                relations = []
                ID = 1

            rel = create_relation(ref_line, ID)
            relations.append(rel)

        with open(pub_annot_folder+'/'+ref_line['']) as outfile:
            out_file.write(json.dumps(data))



        
    
    
