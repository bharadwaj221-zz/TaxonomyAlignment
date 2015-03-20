# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 21:15:07 2015

@author: bharadwaj
"""

import pickle,sys
domain=sys.argv[1]
crumbs=pickle.load(open('Data/'+domain+'_CRUMBS.p'))

catMap={}
for c in crumbs:
    root=c.split('>')[0].strip().lower()
    if not catMap.has_key(root):
        catMap[root]=1
    else:
        catMap[root]+=1

pickle.dump(catMap,open(domain+'_CAT_MAP.p','wb'))