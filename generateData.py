# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 10:18:52 2014

@author: bharadwaj
"""

import sys, pickle
Crumbs=[]
Titles=[]
domain=sys.argv[2]
count=0
with open(sys.argv[1]) as inputFile:
    for line in inputFile:
        count+=1
        
        parts=line.strip().split('\t')
        if len(parts)>=3 and '>' in parts[2] and domain.lower() in parts[0].lower():
            Titles.append(parts[1].strip())
            Crumbs.append(parts[2].strip())
        if count%1000000==0:
            print count,'lines read', parts[1], parts[2]
                
            
pickle.dump(Titles,open('Data/'+domain+'_TITLES.p','wb'))
pickle.dump(Crumbs,open('Data/'+domain+'_CRUMBS.p','wb'))
    
        

        
        
            
    
