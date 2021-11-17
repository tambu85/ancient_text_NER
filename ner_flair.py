#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NER with flair
"""
import sys
import os
from flair.data import Sentence
from flair.models import SequenceTagger
import pandas as pd

history='ghewond'
    
path = os.getcwd()+'/data/'+history+'/'

for filename in os.listdir(path):
    print(filename)
    with open(path+filename, 'r') as f: 
        data = f.read()#.replace('\n', '')
   
    sentence=Sentence(data)
    
    # load the NER tagger
    tagger = SequenceTagger.load('ner')

    # run NER over sentence
    tagger.predict(sentence)   
    
    ent_dict=sentence.to_dict(tag_type='ner') 
    
    loc_df=pd.DataFrame(columns=['text_name', 'start', 'end', 'type','rho'])
      
    for e in ent_dict['entities']:
            if(e['type']=="GPE" or e['type']=="LOC"):
                loc_df = loc_df.append({'text_name': e['text'], 
                                                'start': e['start_pos'],
                                                'end': e['end_pos'],
                                                'type': e['type'],
                                                'rho':e['confidence']}, 
                                                ignore_index=True)
          
     
    output_path=os.getcwd()+"/output/"+history+"/output_flair/"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_flair = open(output_path+os.path.splitext(filename)[0]+'_flair_entities.csv','w+')
    loc_df.to_csv (output_flair, header=True)
        
    
sys.stdout.write("Done!")
