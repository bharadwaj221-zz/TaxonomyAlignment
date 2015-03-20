# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 09:54:37 2014

@author: bharadwaj
"""
import sys,pickle,string, re
level=int(sys.argv[2])
domain=sys.argv[1]
Crumbs=pickle.load(open('Data/'+domain+'_CRUMBS.p'))
rootCatMap=pickle.load(open(domain+'_CAT_MAP.p'))
print 'Data Loaded'
Categories=[]
count=0
for crumb in Crumbs:
    count+=1
    if count%10000000==0:
        print count, ' lines read' 
    l=-1
    parts=crumb.split('>')
    
    root=parts[0].strip()
    child=parts[1].strip()
    flag=False
    if domain in root.lower() or rootCatMap.has_key(child):
        flag=True
    if flag==True:
        l=level+1
    else:
        l=level
    if len(parts) <l+1:
        continue
    cat=parts[l].strip().lower()
    cat=cat.translate(None,string.punctuation)
    if not Categories.__contains__(cat):
        
        Categories.append(cat)
        
pickle.dump(Categories,open('level'+str(level+1)+'/'+domain+'_Level'+str(level)+'_Categories.p','wb'))
    