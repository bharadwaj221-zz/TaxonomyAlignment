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
import re
import gevent
from parallel import *
from multiprocessing import Pool, Process
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.svm import LinearSVC
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import make_scorer

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
        
    
rootCatMap=pickle.load(open(domain+'_CAT_MAP.p'))








     

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
        
        
        
        
        pickle.dump(RData,open('level'+str(level)+'/DATA_'+domain+'_'+parent+'.p','wb'))
        pickle.dump(CAT_MAP[parent],open('level'+str(level)+'/'+domain+'_'+parent+'_CAT_MAP.p','wb'))
        pickle.dump(LABEL_DICT[parent],open('level'+str(level)+'/'+domain+'_'+parent+'_LABEL_DICT.p','wb'))
        pickle.dump(LABEL_MAP[parent],open('level'+str(level)+'/'+domain+'_'+parent+'_LABEL_MAP.p','wb'))
#   
    
    limit=int(sys.argv[3])
#    limit=10
    for parent in LABELS:
        labelDict=LABEL_DICT[parent]       
        examples=[]
        labels=[]
        for j in range(len(LABELS[parent])):
            if labelDict[LABELS[parent][j]] >limit:
                examples.append(DATA[parent][j])
                labels.append(LABELS[parent][j])
        DATA[parent]=examples
        LABELS[parent]=labels
        n=len(DATA)
    print 'Data Loaded ',n
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
    
    print "\n\nSTARTING TRAINING FOR CLASSIFIER PARENT = "+str(parent)
    
    
    
    #examples=DATA[parent]
    labels=LABELS[parent]
    yset=list(set(labels))
    labels=numpy.array(labels)  
    
    print 'Generated data & labels', numpy.shape(labels),' @ ',time.strftime("%H:%M:%S")
    fout=open('TaxonomyAlignment/reports/level'+str(level)+'/'+domain+'_'+'Level_'+str(level)+'_Results_'+parent+'.txt','wb')
    suff_data=int(sys.argv[3])
    if len(parent   )==0:
        pout=open('level'+str(level)+'/STATUS/status','wb')
    else:
        pout=open('level'+str(level)+'/STATUS/'+domain+'_'+parent,'wb')
    #if(len(labels)<5):     
    if(len(labels)<suff_data): 
        fout.write('Insufficient data for '+parent+' '+ str(len(labels)))        
        fout.close()
        print 'Insufficient data for '+parent+' '+ str(len(labels))
        pout.write("-1")
        pout.close()
        
        return
    
    elif len(yset)<=1:
        fout.write('Only one label data for '+parent+' = '+str(yset))        
        fout.close()
        print 'Only one label data for '+parent+' = '+str(yset)
        pout.write("-1")
        pout.close()
        
        return
    else:
        fmax=0.0
        
        folds=5
        trainingAccuracy = numpy.zeros(folds)
        trainingBaseline = numpy.zeros(folds)
        testingAccuracy = numpy.zeros(folds)
        testingBaseline = numpy.zeros(folds)
        testingDensity = numpy.zeros(folds)
        testingF1 = numpy.zeros(folds)
        skf = StratifiedKFold(labels, folds)
    
    
        fmax=0
        for j in range(0,1):

            c=10**j
            classifier = LinearSVC(multi_class='ovr',C=c)
            for i, (train, test) in enumerate(skf):
                 file='TaxonomyAlignment/reports/level'+str(level)+'/'+domain+'_report_'+str(j)+'_'+str(i+1)+'.txt'
                 vout=open(file,'wb')
                 
                 fout.write('Iteration no '+str(i)+' @ '+str(time.strftime("%H:%M:%S"))+'\n')
                 
                 print 'Iteration no ',str(i),' @ ',str(time.strftime("%H:%M:%S"))
                 
                 vectorizer = CountVectorizer(min_df=1,dtype='double')
                 normalizer = Normalizer()
                 X = normalizer.fit_transform(vectorizer.fit_transform(select(DATA[parent],train)))
                 print 'Generated data', numpy.shape(X),' @ ',time.strftime("%H:%M:%S")
                 
                 
                 #print 'Labels = ',numpy.shape(labels)
        
                    
                #    vectorizer = CountVectorizer(min_df=1,dtype='double')
                #    normalizer = Normalizer()
                #    classifier = LinearSVC(multi_class='ovr')
                #    strawMan = DummyClassifier(strategy='most_frequent')
                
                    
                    
                              
                 
                 y = labels[train]
                 yset=set(y)
                 if len(yset)<=1:
                     continue
             
                 print 'Generated labels', len(y), ' @ ',time.strftime("%H:%M:%S")
                 
                 classifier.fit(X,y)
                    
                 print 'Grid Searched and Trained classifier',' @ ',time.strftime("%H:%M:%S")
                    
                #
                #    testingDensity[i] = computeDensity(vectorizer, select(examples,test))
                 
                 trainingAccuracy[i] = accuracy_score(y,classifier.predict(X)) # predict(classifier,select(examples,train), labels[train], vectorizer, normalizer)
                 print 'Training Accuracy',trainingAccuracy[i]
                    
                 testingAccuracy[i] = predict(classifier,select(DATA[parent],test), labels[test],vectorizer,normalizer, i + 1, True)
                 print 'Test Accuracy',testingAccuracy[i]
                 testingF1[i] = predictF1(classifier,select(DATA[parent],test), labels[test],vout,vectorizer,normalizer)
                 print 'Test f1',testingF1[i]
                 print 'Iteration '+str(i)+' done'
                 fout.write('Iteration '+str(i)+' done'+'\n')
                 vout.close()
                 if testingF1[i]  >=fmax: 
                     fmax=testingF1[i]
                     accMax=trainingAccuracy[i]
                     testAccMax=testingAccuracy[i]
                     cmax=classifier
                     vmax=vectorizer
                     nmax=normalizer
        print "FINAL RESULTS:"+ parent+"\n"
        print "Training Accuracy:" , accMax
        print "Test Accuracy:" , testAccMax
        print "Testing F1:" , fmax
        print ' @ '+time.strftime("%H:%M:%S")
        fout.write("\n\nFINAL RESULTS "+parent+" :\n")    
        fout.write("Training Accuracy:" + str(accMax)+'\n')
        fout.write("Test Accuracy:" + str(testAccMax)+'\n')
        fout.write("Testing F1:" + str(fmax)+'\n')
    
        print '\nBest Classifier for '+parent+' : '
        print cmax  
        fout.write('\nBest Classifier for '+parent+' : \n')  
        fout.write(str(cmax))
        pickle.dump(cmax,open('level'+str(level)+'/'+domain+'_'+parent+'_CMAX.p','wb'))
        pickle.dump(vmax,open('level'+str(level)+'/'+domain+'_'+parent+'_VMAX.p','wb'))
        pickle.dump(nmax,open('level'+str(level)+'/'+domain+'_'+parent+'_NMAX.p','wb'))

    fout.write('\n'+parent+'   SUCCESS!!!!!!!\n\n')
    print parent, ' SUCCESS!!!'
    fout.close()
    pout.write('1')
    pout.close()
#
#    return str(testingF1.mean())
    return '0'


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

for level in range(1):
    
    print 'Starting Training for level ', level
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
    
    
    start=time.time()
    Pr=pool.map(fnTrain,parents)
    
    
    end=time.time()    
    
    tout=open('level'+str(level)+'/TIME_TAKEN.txt','wb')
    print 'Time Taken = ',str(end-start), ' s'
    tout.write('Classifiers = '+str(n)+' Time Taken = '+str(end-start)+ ' s')
    tout.close()
print 'Completed...'
    