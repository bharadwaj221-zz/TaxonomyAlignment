# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 19:34:57 2015

@author: bharadwaj
"""

import pickle,sys

domain=sys.argv[1]
Crumbs=pickle.load(open('Data/'+domain+'_CRUMBS.p'))

maxLevels=0
Concepts={}
LeafConcepts={}
for c in Crumbs:
  parts=c.split('>')  
  if len(parts)> maxLevels:
      maxLevels=len(parts)
  for j in range(len(parts)):    
      if not Concepts.has_key((j,parts[j].strip().lower())):
         Concepts[(j,parts[j].strip().lower())]=True
  if not LeafConcepts.has_key(c.strip().lower()):
        LeafConcepts[c.strip().lower()]=1       
  else:
        LeafConcepts[c.strip().lower()]+=1                


print 'No of concepts= ',len(Concepts)
print 'max no of levels = ', maxLevels
print 'no of leaf concepts = ',len(LeafConcepts)
print 'no of instances = ',len(Crumbs)

mn=9999999999
mx=0

for lc in LeafConcepts:
    if LeafConcepts[lc]>mx:
        mx=LeafConcepts[lc]
    if LeafConcepts[lc]<mn:
        mn=LeafConcepts[lc]
        

print 'max no of instances per leaf = ',mx
print 'min no of instances per leaf = ',mn
          
          
