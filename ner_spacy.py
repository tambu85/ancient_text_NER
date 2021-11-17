# -*- coding: utf-8 -*-
"""
NER with spacy
"""
import sys
import spacy
import en_core_web_sm
import pandas as pd


with open("/data/all_texts/ghewond_all.txt", 'r') as file:
    data = file.read()

nlp = spacy.load('en_core_web_sm')
doc = nlp(data)

loc_df=pd.DataFrame(columns=['text_name', 'start', 'end', 'type'])

for e in doc.ents:
    if(e.label_=="GPE" or e.label_=="LOC"):
        loc_df = loc_df.append({'text_name': str(e), 
                                        'start': e.start,
                                        'end': e.end,
                                        'type': e.label_}, 
                                        ignore_index=True)
    
loc_df.to_csv ('/output/all/ghewond_spacy_entities.csv', header=True)
sys.stdout.write("Done!")
