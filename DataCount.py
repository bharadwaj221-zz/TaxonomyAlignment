# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 17:46:00 2015

@author: bharadwaj
"""

import pickle, sys
DataMap={}
count=0
fin = open('Data/masterData.tsv')
for line in fin:
    count+=1
    parts=line.strip().split('\t')
    if len(parts)>=3 and '>' in parts[2]:
        domain=parts[0].split('.')[1].strip().lower()
        if count%10000000==0:
            print count,' lines read ', domain, parts[0]
        if DataMap.has_key(domain):
            DataMap[domain]+=1
        else:
            DataMap[domain]=1
        
        
        if domain=='amazon' and parts[2].strip().lower().startswith('books'):
            print parts[2]


print'\n\n Details'


fout=open('Data/DATA_MAP.txt','wb')
for dom in DataMap:
    if DataMap[dom]>50000:
        print dom, DataMap[dom]
        fout.write(dom+'\t'+str(DataMap[dom])+'\n')
fout.close()
pickle.dump(DataMap,open('Data/DATA_MAP.p','wb'))

