# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 15:32:17 2015

@author: bharadwaj
"""
import pickle,sys, string
Crumbs=pickle.load(open('Data/'+sys.argv[1]+'_CRUMBS.p'))
Titles=pickle.load(open('Data/'+sys.argv[1]+'_TITLES.p'))
crumbs=[]
titles=[]
if len(Crumbs)!= len(Titles):
    print 'Data corrupted'
    exit
for i in range(len(Crumbs)):
    s=Crumbs[i]
    
    if '>' not in s or ';' in s:
        
        continue
    parts=s.split('>')
    if '\xc3\xa9' in s:
        s=string.replace(s,'\xc3\xa9','e')
    
    if ',' in s:
        s=string.replace(s,',','')
    if '/' in s:
        s=string.replace(s,'/','')
    if '\'' in s:
        s=string.replace(s,'\'','')
    flag=False
    for p in parts:
        if len(p.strip())<1:
            print s
            flag=True
            break
    if flag:
        continue
        
    if s.startswith('Amazon.com') or s.startswith('>') or s.lower().startswith('best buy'):    
        s=(s.partition('>')[2])
        
    
    if s.endswith('>'):
        s=s[:-1]
        print s,"end"
    crumbs.append(s)
    titles.append(Titles[i])

pickle.dump(crumbs,open('Data/'+sys.argv[1]+'_CRUMBS.p','wb'))
pickle.dump(titles,open('Data/'+sys.argv[1]+'_TITLES.p','wb'))