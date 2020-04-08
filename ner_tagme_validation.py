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

df_columns = ['text_name', 'start', 'end', 'entity_name', 'rho','link_prob', 'lon','lat', 'correct']

user_end = False
for filename in os.listdir(path_text):
    if user_end:
        print("User requested stop")
        break
    print("*************")
    print("VALIDATION NER file:"+filename)
    file_output=os.path.splitext(filename)[0]+'_entities.csv'
    validation_output = file_output.replace('entities', 'entities_validated')
    # Read the original text file
    with open(path_text+filename, 'r') as t:
        text = t.read()#.replace('\n', '')
    print("")
    print(text)
    # Read the file of generated entities
    with open(path_output+file_output, 'r') as f_out:
        loc_df = pd.read_csv(f_out)

    # Read the file of already-validated entities, if it exists
    try:
        with open(path_output+validation_output, 'r') as fv_out:
            output_df = pd.read_csv(fv_out)
    except FileNotFoundError:
        output_df=pd.DataFrame(columns=df_columns)#,'num_occ','num_dect'])

    bookmark=0

    for i,e in loc_df.iterrows():
        if user_end:
            break

        # Do we already have an answer?
        try:
            found = output_df.loc[i]
        except KeyError:
            found = None
        if found is not None:
            bookmark=e['end']+1
            continue

        end = e['end']
        print(text[bookmark:end+20])

        print("Text entity:"+e['text_name'])
        print("Geo entity:"+e['entity_name']+", coordinates: ("+str(e['lon'])+","+str(e['lat'])+")")
        response_valid = False
        while not response_valid:
            print("Is it correct? (1=Yes,0=No)")
            response = input()
            if(response==str(1) or response=="y"):
                response_valid = True
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

                bookmark=end+1
            elif(response==str(0) or response=="n"):
                response_valid = True
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
            elif(response=="q"):
                # End the loop and write out what we have
                response_valid = True
                user_end = True

    #print(loc_df)
    # Only write an output file if it has content
    if output_df.size > 0:
        output_df.to_csv(path_output+validation_output, header=True)
