
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
NER with nltk
"""
import sys
import slate3k as slate
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import TreebankWordTokenizer
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import pandas as pd


    
with open("data/all_texts/ghewond_all.txt", 'r') as file:
    data = file.read()#.replace('\n', '')
    
spans=list(TreebankWordTokenizer().span_tokenize(str(data)))
tokens=list(TreebankWordTokenizer().tokenize(str(data)))
#tokens=nltk.word_tokenize(str(data))
pos_tags=nltk.pos_tag(tokens)
ne_tree = nltk.ne_chunk(pos_tags,binary=False)



index=0
loc_df=pd.DataFrame(columns=['text_name', 'start', 'end', 'type'])

for chunk in ne_tree:
    if hasattr(chunk, 'label'):
        len_chunk=len(nltk.word_tokenize(str(chunk)))-3 #-3 because of 2 parenthesis and 1 label
        if(chunk.label() == 'GPE' or chunk.label() == 'LOC'):
            begin_pos = spans[index][0]      
            end_pos = spans[index][1]+len_chunk
            loc_df = loc_df.append({'text_name': tokens[index:index+len_chunk], 
                                    'start': begin_pos,
                                    'end': end_pos,
                                    'type': chunk.label()}, 
                                    ignore_index=True)
    
        index += len_chunk
        
    else:
        index += 1


loc_df.to_csv ('/output/all/ghewond_NLTK_entities.csv', header=True)
 
    
sys.stdout.write("Done!")


