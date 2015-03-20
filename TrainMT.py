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
domain=sys.argv[1]
vout=open('test.txt','a')
vout.write(sys.argv[1]+' '+sys.argv[2])
vout.close()
Crumbs=pickle.load(open('Data/'+domain+'_CRUMBS.p'))

Titles=pickle.load(open('Data/'+domain+'_TITLES.p'))
fmax=0
        
    
rootCatMap=pickle.load(open(domain+'_CAT_MAP.p'))
level=int(sys.argv[2])
def getLabel(level, allLabels,  category):
    
    
    if category in allLabels[level]:
        
        return allLabels[level][category]
    else:
        return '###'


#def trainAny(parent, level, allLabels):
#    parLabel=allLabels[level][parent]

     

def readExamples(parent):
    queries = []
    
    
    #allLabels = pickle.load(open(domain+'_LABELS.p'))
    
    #parent=parent.translate(None,string.punctuation)
    #allLabels = pickle.load(open(domain+'_LABELS.p'))
    labelDict = {}
    catMap = {}
    
    
    labels = []
    
    currLabel=1
    
    
    for i in range(0,len(Crumbs)):
            
                
            
                
                
                title = Titles[i]
                crumb = Crumbs[i]
                if ">" in crumb:
                    parts = crumb.split('>')
                    root=parts[0].strip().lower()
                    child=parts[1].strip().lower()
                    if len(parts)<level+1:
                        continue
                    par=parts[level-1].strip().lower()
                    category=parts[level].strip().lower()
                    if len(parts) > level+1:                    
                        nextCat=parts[level+1].strip().lower()                    
                    else:
                        nextCat='###'
                    child=child.translate(None,string.punctuation)    
                    category=category.translate(None,string.punctuation)    
                    nextCat=nextCat.translate(None,string.punctuation)
                    
                    if rootCatMap.has_key(child):
                        flag=True
                        #print "Corrected bread crumb:",title, crumb
                        
                    else:
                        flag=False                    
                    
                    if len(root)==0 or root.lower() == 'amazon.com' or flag==True:
                        par = category
                        if nextCat=='###': 
                            continue
                        category=nextCat
                    
                    
                    if level!=0 and par != parent:
                        #print 'here'
                        continue                 
                    
                    
                    
                    
                    if catMap.has_key(category):
                        label=catMap[category]
                    else:
                        catMap[category]=currLabel
                        label=currLabel
                        currLabel+=1
                    if labelDict.has_key(label):
                        labelDict[label]+=1
                    else:
                        labelDict[label]=1
                    
                    #label = getLabel(level, allLabels, category)
                    #label = getLabel(level, allLabels, crumb)
                    #if label in labelDict and labelDict[label]>1000:
                    title=title.translate(None,string.punctuation).translate(None,string.digits)
                    title=re.sub(' [a-zA-Z]| [a-zA-Z]',' ',title)
                    queries.append(title)
                    labels.append(label)
    
    pickle.dump(catMap,open('level'+str(level)+'/'+domain+'_'+parent+'_CAT_MAP.p','wb'))
    pickle.dump(labelDict,open('level'+str(level)+'/'+domain+'_'+parent+'_LABEL_DICT.p','wb'))
#   
    Labels=[]
    Queries=[]
    limit=int(sys.argv[3])
    for i in range(0,len(labels)):
        if(labelDict[labels[i]]>limit):
            Queries.append(queries[i])
            Labels.append(labels[i])
    return Queries, Labels



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
    
def AvgF1(y1,y2):
    file='TaxonomyAlignment/reports/level'+sys.argv[2]+'/report_'+parents[p-1]+'.txt'
    vout=open(file,'wb')
    vout.write(classification_report(y1,y2))
    vout.close()
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


def fnTrain(parent,examples, labels):
    
    print "\n\nSTARTING TRAINING FOR CLASSIFIER PARENT = "+str(parent)
    
    
    
    
    yset=list(set(labels))
    
    labels=numpy.array(labels)  
    folds=3
    print 'Generated data & labels', numpy.shape(labels),' @ ',time.strftime("%H:%M:%S")
    fout=open('level'+str(level)+'/Level_'+str(level)+'_Results_'+parent+'.txt','wb')
    if len(parent   )==0:
        pout=open('level'+str(level)+'/STATUS/status','wb')
    else:
        pout=open('level'+str(level)+'/STATUS/'+parent,'wb')
    if(len(labels)<100):     
    #if(len(labels)<20): 
        fout.write('Insufficient data for '+parent)        
        fout.close()
        print 'Insufficient data for '+parent
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
        print len(yset)
        c=1
        
        fmax=0
        folds=3
        skf = StratifiedKFold(labels, folds)
        trainingAccuracy=0
        testingF1 = numpy.zeros(folds)
        
        vectorizer = CountVectorizer(min_df=1,dtype='double',stop_words='english')
        normalizer = Normalizer(norm='l1')
        
        #for i, (train, test) in enumerate(skf):         
        for i in range(0,1):
            
            classifier = LinearSVC(multi_class='ovr')
#            file='TaxonomyAlignment/reports/level'+str(level)+'/report_'+parent+'_'+str(i+1)+'.txt'
            
            fout.write('Iteration no '+str(i)+' @ '+str(time.strftime("%H:%M:%S"))+'\n')
             
            print '\nIteration no ',str(i),' @ ',str(time.strftime("%H:%M:%S"))
#            data=select(examples,train)
            data=examples
#            y = labels[train]
            y=labels
            yset=list(set(y))
            if len(yset)==1:
                continue
            
            trainData = normalizer.fit_transform(vectorizer.fit_transform(data))
            print 'Generated data', numpy.shape(trainData),' @ ',time.strftime("%H:%M:%S")
            X=trainData                 
            
            yset=set(y)
            clist=[]
            for j in range(0,1):
                clist.append(10**j)
            F1=make_scorer(AvgF1)
            clf=GridSearchCV(classifier,[{'C':clist}],scoring=F1, cv=skf, n_jobs=3)            
            
            
            clf.fit(X,y)
            
            
            #gevent.sleep(1)
            
#            gevent.sleep(0.5)
                        
            print 'Trained classifier',' @ ',time.strftime("%H:%M:%S")
                        
                    #
                    #    testingDensity[i] = computeDensity(vectorizer, select(examples,test))
            pred=clf.predict(X)
            
            
            trainingAccuracy = accuracy_score(y,pred) 
            print 'Training Accuracy',trainingAccuracy
            print 'Test f1:'+str(clf.best_score_)
                
#            testingAccuracy[i] = predict(clf,select(examples,test), labels[test],vectorizer,normalizer, i + 1, True)
#            print 'Test Accuracy',testingAccuracy[i]
#            testingF1[i] = predictF1(clf,select(examples,test), labels[test],vout,vectorizer,normalizer)
#            print 'Test f1',testingF1[i]
            
            
            print 'Iteration '+str(i)+' done'
            fout.write('Iteration '+str(i)+' done'+'\n')
            
    fout.write("\n\nFINAL RESULTS "+parent+" :\n")    
    fout.write("Training Accuracy:" + str(trainingAccuracy)+'\n')
    fout.write('Test f1:'+str(clf.best_score_)+'\n')
    
    
    cmax=clf
    vmax=vectorizer
    nmax=normalizer
    print "\n\nFINAL RESULTS:\n"
    print "Training Accuracy:" + str(trainingAccuracy)
    
    print "Testing F1:" + str(clf.best_score_)
    print ' @ '+time.strftime("%H:%M:%S")
        
    
    print '\nBest Classifier for'+parent+' : '
    print cmax  
    fout.write('\nBest Classifier for '+parent+' : \n')  
    fout.write(str(cmax))
    pickle.dump(cmax,open('level'+str(level)+'/'+parent+'_CMAX.p','wb'))
    pickle.dump(vmax,open('level'+str(level)+'/'+parent+'_VMAX.p','wb'))
    pickle.dump(nmax,open('level'+str(level)+'/'+parent+'_NMAX.p','wb'))

    fout.write(parent+'   SUCCESS!!!!!!!\n\n')
    print parent, ' SUCCESS!!!'
    fout.close()
    pout.write('1')
    pout.close()
#
#    return str(testingF1.mean())
    return '0'


#####################     MAIN




if level!=0:
    parents=pickle.load(open('level'+str(level)+'/'+domain+'_Level'+str(level-1)+'_Categories.p'))
else:
    parents=['']







examples=[]
labels=[]
threads=[]
data=[]
start=time.time()







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
p=int(sys.argv[4])

e,l=readExamples(parents[p-1])    
#examples.append(e)
#labels.append(l)


#for i in xrange(len(parents)):
#    t=(gevent.spawn(fnTrain,parents[i],examples[i],labels[i]))
#    gevent.sleep(0)
#    threads.append(t)
#gevent.joinall(threads)
#

#
fnTrain(parents[p-1],e,l)
##



end=time.time()



print 'END OF PARENT ',p-1




#
#for s in scores:
#    print s


# seq 10 | parallel -j 4 python2.7 level2/LevelTwoTrainMT.py amazon 
