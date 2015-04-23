# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 21:10:12 2014

@author: bharadwaj
"""

__author__ = 'bharadwaj'



import sys


import numpy
import time
import string


from multiprocessing import Pool
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.svm import LinearSVC


from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report

import pickle






#level=int(sys.argv[1])
#k=str(level)
domain=sys.argv[1]





Crumbs=pickle.load(open('Data/'+domain+'_CRUMBS.p'))

Titles=pickle.load(open('Data/'+domain+'_TITLES.p'))
if len(Crumbs)!=len(Titles):
    print 'Data Corrupted' 
    exit
if len(Crumbs) > 1000000:
    Crumbs=Crumbs[1:1000000]
    Titles=Titles[1:1000000]
fmax=0
        
    







     

def readExamples(level):
    
    
    #allLabels = pickle.load(open(domain+'_LABELS.p'))
    
    #parent=parent.translate(None,string.punctuation)
    #allLabels = pickle.load(open(domain+'_LABELS.p'))
    labelDict = {}
    catMap = {}
    
    
    labels = []
    
    currLabel={}
    
    
    n=0
    for i in range(0,len(Crumbs)):
            

    
            
                
                
                title = Titles[i].strip().lower()
                crumb = Crumbs[i]
                if '/' in crumb:
                        crumb=string.replace(crumb,'/','')
                if ">" in crumb:
                    parts = crumb.split('>')
                    if len(parts)<=level:
                        continue
#                    root=parts[0].strip().lower()
#                    child=parts[1].strip().lower()
#                    if len(parts)<level+1:
#                        continue
                    if level==0:
                            par=''
                    else:
                        par=parts[level-1].strip().lower()
                    category=parts[level].strip().lower()
#                    if len(parts) > level+1:                    
#                        nextCat=parts[level+1].strip().lower()                    
#                    else:
#                        nextCat='###'
#                        
#                    if rootCatMap.has_key(child):
#                        flag=True
#                        #print "Corrected bread crumb:",title, crumb
#                        
#                    else:
#                        flag=False                    
#                    
#                    if len(root)==0 or root.lower() == 'amazon.com' or flag==True:
#                        par = category
#                        if nextCat=='###': 
#                            continue
#                        category=nextCat
#                                        
                    
                    if not DATA.has_key(par):
                        #print 'here'
                        DATA[par] = []
                        LABELS[par]=[]
                        LABEL_DICT[par]={}
                        CAT_MAP[par]={}
                        LABEL_MAP[par]={}
                    
                    catMap=CAT_MAP[par]
                    labelMap=LABEL_MAP[par]
                    if catMap.has_key(category):
                        label=catMap[category]
                    else:
                        if not currLabel.has_key(par):
                            currLabel[par]=1
                        catMap[category]=currLabel[par]
                        label=currLabel[par]
                        labelMap[label]=category
                        currLabel[par]+=1
                    CAT_MAP[par]=catMap
                    LABEL_MAP[par]=labelMap
                    labelDict=LABEL_DICT[par]
                    if labelDict.has_key(label):
                        labelDict[label]+=1
                    else:
                        labelDict[label]=1
                    LABEL_DICT[par]=labelDict
                    
                    #label = getLabel(level, allLabels, category)
                    #label = getLabel(level, allLabels, crumb)
                    #if label in labelDict and labelDict[label]>1000:
                    title=title.translate(None,string.punctuation).translate(None,string.digits)
#                    if 'baby products' in par:
#                        print 'adding ', title, 'to ', par
                    
                        
                    DATA[par].append(title)
                    LABELS[par].append(label)
                    
    
    for parent in LABELS:
        RData=[]    
        
        for l in LABEL_DICT[parent]:
            data=[]
            for i in range(len(LABELS[parent])):
                if LABELS[parent][i]==l:
                    title=DATA[parent][i]
                    data.append(title)
            RData.append((data,LABEL_MAP[parent][l]))
        
        
        
        
#        pickle.dump(RData,open('level'+str(level)+'/DATA_'+domain+'_'+parent+'.p','wb'))
#        pickle.dump(CAT_MAP[parent],open('level'+str(level)+'/'+domain+'_'+parent+'_CAT_MAP.p','wb'))
#        pickle.dump(LABEL_DICT[parent],open('level'+str(level)+'/'+domain+'_'+parent+'_LABEL_DICT.p','wb'))
#        pickle.dump(LABEL_MAP[parent],open('level'+str(level)+'/'+domain+'_'+parent+'_LABEL_MAP.p','wb'))
#   
    
    limit=int(sys.argv[3])
#    limit=10
    for parent in LABELS:
        labelDict=LABEL_DICT[parent]       
        examples=[]
        labels=[]
        for j in range(len(LABELS[parent])):
            if labelDict[LABELS[parent][j]] >int(sys.argv[4]):
                examples.append(DATA[parent][j])
                labels.append(LABELS[parent][j])
        DATA[parent]=examples
        LABELS[parent]=labels
        n=len(DATA)
#    print 'Data Loaded ',n
    return n
    



def predict(model,examples, actual, vectorizer,normalizer,fold=0, dump=False):
    X = normalizer.transform(vectorizer.transform(examples))
    pred = model.predict(X)
    
    return accuracy_score(actual,pred)

def predictF1(model,examples, actual,vout,vectorizer,normalizer):
    X = normalizer.transform(vectorizer.transform(examples))
    pred = model.predict(X)
    
    vout.write(classification_report(actual,pred))
    
    F= f1_score(actual,pred,average=None)
    meanF=sum(F)/(1.0 * len(F))
    return meanF

#def AvgF1(y1,y2):    
def AvgF1(y1,y2):
    
    F= f1_score(y1,y2,average=None)
    
    meanF=sum(F)/(1.0 * len(F))
    
    return meanF


def prettyPrint(givenVector):
    return "%.4f" % givenVector.mean() +  "(" +"%.4f" % givenVector.std() + ")"
    
def select(arr,index):
    res=[]    
    for i in index:
        res.append(arr[i])
    return res

def classifier_fit(model,X,y):
    model.fit(X,y)
    return model


def fnTrain(parent):
    
    
    
    
    #examples=DATA[parent]
    labels=LABELS[parent]
    yset=list(set(labels))
    labels=numpy.array(labels)  
    a=0
    b=0
#    print 'Generated data & labels', numpy.shape(labels),' @ ',time.strftime("%H:%M:%S")
    suff_data=int(sys.argv[3])
    
    #if(len(labels)<5):     
    if not (len(labels)<suff_data) and not len(yset)<=1:
        
#        print 'Only one label data for '+parent+' = '+str(yset)
        
    
        
        a+=1
        b+=len(yset)

    return (a,b)        
            
            

#####################     MAIN












#parents=parents[1:10]





#for parent in parents:
#     d=gevent.spawn(readExamples,parent)
#     gevent.sleep(0)
#     data.append(d)
#     
#gevent.joinall(data)    
#for i in xrange(len(data)):
#    examples.append(data[i].value[0])
#    labels.append(data[i].value[1])
#

#
parents=[]

for level in range(10):
    
    
    DATA={}
    LABELS={}
    LABEL_DICT={}
    LABEL_MAP={}
    CAT_MAP={}
    Pr=[]
    
    n=readExamples(level)
    if level>0 and n<=1:
        break
    parents=[]
    for p in DATA:
        parents.append(p)
        
    nproc=int(sys.argv[2])
    pool=Pool(processes=nproc)
    
    
    
    classes=0
    classifiers=0
    for p in parents:
        a,b=fnTrain(p)
        classifiers+=a
        classes+=b
    if classifiers==0:
        break
    print     'Level = ',level,'Avg classes = ',str(classes/(1.0*classifiers)), 'classifiers = ', classifiers
    
    
    
    
print 'Completed...'
    