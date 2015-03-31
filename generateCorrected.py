# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 15:32:17 2015

@author: bharadwaj
"""
import pickle,sys, string
domain=sys.argv[2]
mn=int(sys.argv[3])
#Crumbs=pickle.load(open('Data/'+domain+'_CRUMBS.p'))
#Titles=pickle.load(open('Data/'+domain+'_TITLES.p'))

def correctCrumb(s):
    
    if '>' not in s or ';' in s:
        
        return ''
    if '\xc3\xa9' in s:
        s=string.replace(s,'\xc3\xa9','e')
    
    if ',' in s:
        s=string.replace(s,',','')
    if '/' in s:
        s=string.replace(s,'/','')
    if '\'' in s:
        s=string.replace(s,'\'','')
    
        
    if s.lower().startswith('amazon.com') or s.startswith('>') or s.lower().startswith('online shopping'):    
        s=(s.partition('>')[2])
    if s.endswith('>'):
        s=s[:-1]
        
    parts=s.split('>')
    
    for p in parts:
        if len(p)==0:
            return ''
    
        
    s=s.strip()
        
    
    return s

Crumbs=[]
Titles=[]
cdict={}
count=0
with open(sys.argv[1]) as inputFile:
    for line in inputFile:
        count+=1
        
        parts=line.strip().split('\t')
        if len(parts)>=3 and '>' in parts[2] and domain.lower() in parts[0].lower():
            crumb=parts[2].strip()
            crumb=correctCrumb(crumb)            
            if crumb == '':
                continue
            else:
                Titles.append(parts[1].strip())
                Crumbs.append(crumb)
                if cdict.has_key(crumb):
                    cdict[crumb]+=1
                else:
                    cdict[crumb]=1
                
        if count%1000000==0:
            print count,' lines read'



crumbs=[]
titles=[]
for i in range(len(Crumbs)):
    if cdict[Crumbs[i]]>mn:
        crumbs.append(Crumbs[i])
        titles.append(Titles[i])

print 'SIZE = ',len(crumbs)

pickle.dump(crumbs,open('Data/'+sys.argv[2]+'_CRUMBS.p','wb'))
pickle.dump(titles,open('Data/'+sys.argv[2]+'_TITLES.p','wb'))