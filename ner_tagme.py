#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 10:33:08 2020

@author: marcella
"""
import sys
import os
import modif_tagme
import requests
import pandas as pd
import folium
from urllib import error
from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import EndPointNotFound, EndPointInternalError,SPARQLWrapperException
import time


def get_coordinates(id):
    url = "https://en.wikipedia.org/w/api.php?action=query&prop=coordinates&format=json&pageids="+str(id)
    r = requests.get(url)
    json_data = r.json()
    path=json_data['query']['pages'][str(id)]
    if('coordinates' in path):
        coord= path['coordinates']
    else:
        coord=0
    return(coord)
    
def get_sparql_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    endpoint_sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    endpoint_sparql.setQuery(query)
    endpoint_sparql.setReturnFormat(JSON)
    
    result = None
    try:
      result = endpoint_sparql.query().convert()
    except(error.HTTPError,EndPointInternalError,EndPointNotFound,SPARQLWrapperException) as e: 
        print("error")
        print(e)
        time.sleep(10)
   
    return(result)

    
def is_location(id):
    endpoint_url = "https://query.wikidata.org/sparql"
    query = """SELECT ?item ?is_geo WHERE {
      SERVICE wikibase:mwapi {
        bd:serviceParam wikibase:endpoint "en.wikipedia.org" .
        bd:serviceParam wikibase:api "Generator" .
        bd:serviceParam mwapi:generator "revisions" .
        bd:serviceParam mwapi:pageids \""""+str(id)+"""\".
        ?item wikibase:apiOutputItem mwapi:item .
      }
      BIND ( EXISTS {?item wdt:P31/wdt:P279+ wd:Q618123} AS ?is_geo )
    }
    """
    res = get_sparql_results(endpoint_url, query)

    bool_res=False
    if(res!=None):
        if(res["results"]["bindings"]!=[]):
            res = res["results"]["bindings"][0]['is_geo']['value']
            if(res=='true'):
                bool_res=True

    return(bool_res)


orig_stdout = sys.stdout
access_token="******" #insert yours
modif_tagme.GCUBE_TOKEN = access_token
    
path = os.getcwd()+'/data/single_texts/'
for filename in os.listdir(path):
    print(filename)
    with open(path+filename, 'r') as f:  
    
        text = f.read()#.replace('\n', '')

        loc_df=pd.DataFrame(columns=['text_name', 'start', 'end', 'entity_name', 'rho','link_prob', 'lon','lat'])#,'num_occ','num_dect'])
        ent = modif_tagme.annotate(text)
        ent_dict=ent.original_json['annotations']      

        
        
        for e in ent_dict:
            
            if('title' in e.keys() and e['rho']>0.1 and e['link_probability']>0.05):  

                ent_name = e['title']    
                wid = e['id']
                e_start = e['start']
                e_end = e ['end']

                y=is_location(wid)
                if is_location(wid) :
                    print(ent_name)

                    coord = get_coordinates(wid)
                    if(coord!=0):
                        loc_df = loc_df.append({'text_name': e['spot'], 
                                                'start': e_start,
                                                'end': e_end,
                                                'entity_name': ent_name, 
                                                'rho': e['rho'],
                                                'link_prob': e['link_probability'],
                                                'lon': coord[0]['lon'], 
                                                'lat': coord[0]['lat']}, 
                                                ignore_index=True)
                        print()
                    else:
                        loc_df = loc_df.append({'text_name': e['spot'], 
                                                'start': e_start,
                                                'end': e_end,
                                                'entity_name': ent_name, 
                                                'rho': e['rho'],
                                                'link_prob': e['link_probability'],
                                                'lon': None, 
                                                'lat': None}, 
                                                ignore_index=True)   
        
        
        
        output_path=os.getcwd()+"/output/"+os.path.splitext(filename)[0]
        loc_df.to_csv (output_path+'_entities.csv', header=True)
        
        locations = loc_df.dropna()

        
        # Make an empty map
        m = folium.Map(location=[47, 30], tiles="OpenStreetMap", zoom_start=2)
         
        # I can add marker one by one on the map
        for i in range(0,len(locations)):
            folium.Marker([locations.iloc[i]['lat'],locations.iloc[i]['lon']],popup=locations.iloc[i]['text_name']).add_to(m)
         
        # Save it as html
        m.save(output_path+'_map.html')
    
            
        #mentions = modif_tagme.mentions(text)
        
        #print(mentions)
        
        #for mention in mentions.mentions:
        #    print(mention)
