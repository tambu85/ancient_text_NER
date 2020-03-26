#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 14:31:08 2020

@author: marcella
"""

import sys
import os
import pandas as pd


path_text = os.getcwd()+'/single_texts/'
path_output = os.getcwd()+'/output/'
for filename in os.listdir(path_text):
    print("*************")
    print("VALIDATION NER file:"+filename)
    file_output=os.path.splitext(filename)[0]+'_entities.csv'
    with open(path_text+filename, 'r') as t:
        text = t.read()#.replace('\n', '')
        print("")    
        print(text)
        with open(path_output+file_output, 'r') as f_out:  
            loc_df = pd.read_csv(f_out)
            output_df=pd.DataFrame(columns=['text_name', 'start', 'end', 'entity_name', 'rho','link_prob', 'lon','lat', 'correct'])#,'num_occ','num_dect'])
            
            bookmark=0
            
            for i,e in loc_df.iterrows():
                
                end = e['end']
                print(text[bookmark:end])
                
                print("Text entity:"+e['text_name'])
                print("Geo entity:"+e['entity_name']+", coordinates: ("+str(e['lon'])+","+str(e['lat'])+")")
                print("Is it correct? (1=Yes,0=No)")
                response = input()
                if(response==str(1)):  
                    output_df = output_df.append({'text_name': e['text_name'], 
                                            'start': e['start'],
                                            'end': e['end'],
                                            'entity_name': e['entity_name'], 
                                            'rho': e['rho'],
                                            'link_prob': e['link_prob'],
                                            'lon': e['lon'], 
                                            'lat': e['lat'],
                                            'correct': True}, 
                                            ignore_index=True)
                           
                else:
                    output_df = output_df.append({'text_name': e['text_name'], 
                                            'start': e['start'],
                                            'end': e['end'],
                                            'entity_name': e['entity_name'], 
                                            'rho': e['rho'],
                                            'link_prob': e['link_prob'],
                                            'lon': e['lon'], 
                                            'lat': e['lat'],
                                            'correct': False}, 
                                            ignore_index=True)  
                bookmark=end+1
    
            #print(loc_df)
            
            output_df.to_csv (path_output+os.path.splitext(filename)[0]+'_entities_validated.csv', header=True)
            
    