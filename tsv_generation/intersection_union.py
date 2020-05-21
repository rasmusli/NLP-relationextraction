import pandas as pd
import numpy as np
from pandas import ExcelWriter


def thresh_hold(probability):
    return 1 if probability > 0.5 else 0

def check_union(predictions):
    union = (predictions > 0).any(axis=1)
    return union

def check_intersection(predictions):
    intersection = (predictions > 0).all(axis=1)
    return intersection

predictions = pd.DataFrame()
for i in range(1,11):
    model = 'GAD_'+str(i)
    prediction = pd.read_csv("../subset_predictions/"+model+"/test_results.tsv", delimiter='\t',header=None)
    prediction.columns = ['No Relations', 'Relations']
    index = 0
    for prob in prediction['Relations']:
        predictions.loc[index, model] = thresh_hold(prob)
        index += 1

intersections = check_intersection(predictions)
unions = check_union(predictions)


print(predictions)
writer = ExcelWriter("../subset_predictions/gad_predictions.xlsx")
predictions.to_excel(writer, 'Predictions')
unions.to_excel(writer, 'Union')
intersections.to_excel(writer, 'Intersection')
writer.save()