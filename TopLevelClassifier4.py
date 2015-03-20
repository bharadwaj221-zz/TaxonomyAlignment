__author__ = 'bharadwaj'
import sys


import numpy
import re
import time
import string
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.svm import LinearSVC

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report



import pickle


def getLabel(level, allLabels,  category):
    
    
    if category in allLabels[level]:
        
        return allLabels[level][category]
    else:
        return '###'


#def trainAny(parent, level, allLabels):
#    parLabel=allLabels[level][parent]
       

def readExamples(inputFilename):
    queries = []
    level = 0
    domain=sys.argv[2]
    #allLabels = pickle.load(open(domain+'_LABELS.p'))
    catMap = pickle.load(open(domain+'_CAT_MAP.p'))
    labelDict = pickle.load(open(domain+'_LABEL_DICT.p'))
    mout=open('mapping.txt','wb')
    for i in catMap:
        mout.write(str(i)+'\t'+str(catMap[i])+'\t'+str(labelDict[catMap[i]])+'\n')
    mout.close()
    
    labels = []
    count=0
    
    with open(inputFilename) as inputFile:
        for line in inputFile:
            
                words = line.strip().split('\t')
            
                
                url = words[0]
                title = words[1]
                crumb = words[2]
                if len(words)>=3 and "www.amazon" in url and ">" in crumb:
                    parts = crumb.split('>')
                    category=parts[level].strip().lower()
                    nextCat=parts[level+1].strip().lower()
                    
                        
                    
                    if catMap.has_key(nextCat):
                        flag=True
                        #print "Corrected bread crumb:",title, crumb, url
                        
                    else:
                        flag=False
                    if len(category)==0 or category.lower() == 'amazon.com' or flag==True:
                    
                        category=nextCat
                    
                    #label = getLabel(level, allLabels, crumb)
                    category=category.translate(None,string.punctuation)
                    label=catMap[category]
                    count+=1
                    if count%1000000 == 0:
                        print count, ' lines read', '\t', title
                    if label!='###' and labelDict[label]>1000:
                        title=title.translate(None,string.punctuation).translate(None,string.digits)
                        title=re.sub(' [a-zA-Z]| [a-zA-Z]',' ',title)
                        
                        queries.append(title)
                        labels.append(label)
                        
    
    
    print 'Data read successfully!!!'                   
    return queries, labels

def computeDensity(vectorizer, examples):
    nonZeros  = numpy.apply_along_axis(numpy.sum,1,vectorizer.transform(examples).todense())
    return 1 - numpy.count_nonzero(nonZeros)/float(len(nonZeros))

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

def prettyPrint(givenVector):
    return "%.4f" % givenVector.mean() +  "(" +"%.4f" % givenVector.std() + ")"
    
def select(arr,index):
    res=[]    
    for i in index:
        res.append(arr[i])
    return res

examples, labels = readExamples(sys.argv[1])
#
#
#
#
##
#
##
#
#
vectorizer = CountVectorizer(min_df=1,dtype='double',stop_words='english')
normalizer = Normalizer(norm='l1')
#vectorizer=pickle.load(open('VEC.p'))
#normalizer=pickle.load(open('NORM.p'))
#examples=examples[:10000]
#labels=labels[:10000]


labels=numpy.array(labels)  
print 'Generated labels', numpy.shape(labels),' @ ',time.strftime("%H:%M:%S")
    
##
#pickle.dump(vectorizer,open('VEC.p','wb'))
#pickle.dump(normalizer,open('NORM.p','wb'))
#

print 'Started @ ',time.strftime("%H:%M:%S")






#trainData=trainData[:10000]
#labels=labels[:10000]


folds = 5
skf = StratifiedKFold(labels, folds)
trainingAccuracy = numpy.zeros(folds)
trainingBaseline = numpy.zeros(folds)
testingAccuracy = numpy.zeros(folds)
testingBaseline = numpy.zeros(folds)
testingDensity = numpy.zeros(folds)
testingF1 = numpy.zeros(folds)

fout=open('TaxonomyAlignment/reports/TopLevelResults4.txt','wb')
fmax=0
for j in range(1,3):

    c=10**j
    fout.write('C = '+str(c)+'\n\n')
    classifier = LinearSVC(multi_class='ovr',C=c)
    for i, (train, test) in enumerate(skf):
         file='TaxonomyAlignment/reports/report_c'+str(j+3)+'_'+str(i+1)+'.txt'
         vout=open(file,'wb')
         vout.write('C = '+str(c)+'\n')
         fout.write('Iteration no '+str(i)+' @ '+str(time.strftime("%H:%M:%S"))+'\n')
         
         print 'Iteration no ',str(i),' @ ',str(time.strftime("%H:%M:%S"))
         data=select(examples,train)
         trainData = normalizer.fit_transform(vectorizer.fit_transform(data))
         print 'Generated data', numpy.shape(trainData),' @ ',time.strftime("%H:%M:%S")
         
         
         #print 'Labels = ',numpy.shape(labels)

            
        #    vectorizer = CountVectorizer(min_df=1,dtype='double')
        #    normalizer = Normalizer()
        #    classifier = LinearSVC(multi_class='ovr')
        #    strawMan = DummyClassifier(strategy='most_frequent')
        
            
            
                      
         X=trainData
         y = labels[train]
         yset=set(y)
     
         print 'Generated labels', len(y), ' @ ',time.strftime("%H:%M:%S")
         classifier.fit(X,y)
            
         print 'Grid Searched and Trained classifier',' @ ',time.strftime("%H:%M:%S")
            
        #
        #    testingDensity[i] = computeDensity(vectorizer, select(examples,test))
         
         trainingAccuracy[i] = accuracy_score(y,classifier.predict(X)) # predict(classifier,select(examples,train), labels[train], vectorizer, normalizer)
         print 'Training Accuracy',trainingAccuracy[i]
            
         testingAccuracy[i] = predict(classifier,select(examples,test), labels[test],vectorizer,normalizer, i + 1, True)
         print 'Test Accuracy',testingAccuracy[i]
         testingF1[i] = predictF1(classifier,select(examples,test), labels[test],vout,vectorizer,normalizer)
         print 'Test f1',testingF1[i]
         print 'Iteration '+str(i)+' done'
         fout.write('Iteration '+str(i)+' done'+'\n')
         vout.close()
        #
         
        
    
    fout.write("\nFINAL RESULTS:\n")    
    fout.write("Training Accuracy:" + prettyPrint(trainingAccuracy)+'\n')
    fout.write("Test Accuracy:" + prettyPrint(testingAccuracy)+'\n')
    fout.write("Testing F1:" + prettyPrint(testingF1)+'\n')
    if testingF1.mean() > fmax: 
        fmax=testingF1.mean()
        cmax=classifier
        vmax=vectorizer
        nmax=normalizer
        
    print "FINAL RESULTS:\n"
    print "Training Accuracy:" + prettyPrint(trainingAccuracy)
    print "Test Accuracy:" + prettyPrint(testingAccuracy)
    print "Testing F1:" + prettyPrint(testingF1)
    print ' @ '+time.strftime("%H:%M:%S")
    

print 'Best Classifier: '
print cmax  
fout.write('\nBest Classifier:\n')  
fout.write(str(cmax))
pickle.dump(cmax,open('CMAX.p','wb'))
pickle.dump(vmax,open('VMAX.p','wb'))
pickle.dump(nmax,open('NMAX.p','wb'))

fout.write('SUCCESS!!!!!!!')
fout.close()


