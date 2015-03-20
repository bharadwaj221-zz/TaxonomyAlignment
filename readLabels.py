# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 14:31:44 2014

@author: bharadwaj
"""

import sys
import pickle
import string

def getLabel(level, allLabels, category):
    
    if category in allLabels[level]:
        return allLabels[level][category]
    else:
        return '###'


     

def readLabels(inputFilename):
    
    level = 0
    domain=sys.argv[2]
    #allLabels = pickle.load(open(domain+'_LABELS.p'))
    catMap = {}
    labelDict = {}
    labels = []
    Crumbs=[]
    Titles=[]
    count=0
    currLabel=1
    
    with open(inputFilename) as inputFile:
        for line in inputFile:
                
            
                words = line.strip().split('\t')
            
                
                url = words[0]
                title = words[1]
                crumb = words[2]
                if len(words)>=3 and "www.amazon" in url and ">" in crumb:
                    Crumbs.append(crumb)
                    Titles.append(title)
                    
                    parts = crumb.split('>')
                    category=parts[level].strip().lower()
                    nextCat=parts[level+1].strip().lower()
                    
                    if len(category)==0 or category.lower() == 'amazon.com' or catMap.has_key(nextCat):
                    
                        category=nextCat
                    category=category.translate(None,string.punctuation)    
                    
                    if catMap.has_key(category):
                        label=catMap[category]
                    else:
                        catMap[category]=currLabel
                        label=currLabel
                        currLabel+=1
                    #label = getLabel(level, allLabels, crumb)
                    
                    if labelDict.has_key(label):
                        labelDict[label]+=1
                    else:
                        labelDict[label]=1
                    count+=1
                    if count%1000000 == 0:
                        print count, ' lines read', '\t', title
    
    pickle.dump(labelDict,open('amazon_LABEL_DICT.p','wb'))
    pickle.dump(catMap,open('amazon_CAT_MAP.p','wb'))
    pickle.dump(Crumbs,open('Data/'+domain+'_CRUMBS.p','wb'))
    pickle.dump(Titles,open('Data/'+domain+'_TITLES.p','wb'))
    
                
    return labels,catMap                        
                        




labelDict={}
fout=open('LabelMapping.txt','wb')
fout.write('Label\tCount\tCategory')
labels,catMap = readLabels(sys.argv[1])

for l in labelDict:
    fout.write(str(l)+'\t'+str(labelDict[l])+'\t'+catMap[l]+'\n')
    #print str(l)+'\t'+str(labelDict[l])+'\t'+catMap[l]
fout.close()
