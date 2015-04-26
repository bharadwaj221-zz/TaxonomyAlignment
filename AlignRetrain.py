# -*- coding: utf-8 -*-
"""
Created on Mon Jan  5 15:29:25 2015

@author: bharadwaj
"""
import numpy
import time, string, pickle, sys

from nltk.corpus import wordnet as wn
from multiprocessing import Pool, Process
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import *
from sklearn.svm import LinearSVC
from sklearn.metrics import *



RData=[]    
Data=[]
Parent=[]
Scores=[]
Child={}
Map=[]
vMap=[]
Dup=[]

def select(arr,index):
    res=[]    
    for i in index:
        res.append(arr[i])
    return res
    

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

def fnTrain(parent,level,data,labels):

    domain=sd
    print "\n\nSTARTING TRAINING FOR CLASSIFIER PARENT = "+str(parent)
    yset=list(set(labels))
    labels=numpy.array(labels)  
    suff_data=100
    
    print 'Generated data & labels', numpy.shape(labels),' @ ',time.strftime("%H:%M:%S")
    fout=open('TaxonomyAlignment/reports/level'+str(level)+'/'+domain+'_'+'Level_'+str(level)+'_Results_'+parent+'.txt','wb')
    if len(parent   )==0:
        pout=open('level'+str(level)+'/STATUS/status','wb')
    else:
        pout=open('level'+str(level)+'/STATUS/'+parent,'wb')
    #if(len(labels)<5):     
    if(len(labels)<suff_data): 
        fout.write('Insufficient data for '+parent+' '+ str(len(labels)))        
        fout.close()
        print 'Insufficient data for '+parent+' '+ str(len(labels))
        pout.write("-1")
        pout.close()
        
        return False
    
    elif len(yset)<=1:
        fout.write('Only one label data for '+parent+' = '+str(yset))        
        fout.close()
        print 'Only one label data for '+parent+' = '+str(yset)
        pout.write("-1")
        pout.close()
        
        return False
    else:
        fmax=0.0
        
        folds=3
        trainingAccuracy = numpy.zeros(folds)
        trainingBaseline = numpy.zeros(folds)
        testingAccuracy = numpy.zeros(folds)
        testingBaseline = numpy.zeros(folds)
        testingDensity = numpy.zeros(folds)
        testingF1 = numpy.zeros(folds)
        skf = StratifiedKFold(labels, folds)
    
    
        for i, (train, test) in enumerate(skf):
             file='TaxonomyAlignment/reports/level'+str(level)+'/report_'+parent+'_'+str(i+1)+'.txt'
             vout=open(file,'wb')
             
             fout.write('Iteration no '+str(i)+' @ '+str(time.strftime("%H:%M:%S"))+'\n')
             
             print 'Iteration no ',str(i),' @ ',str(time.strftime("%H:%M:%S"))
             
             vectorizer = CountVectorizer(min_df=1,dtype='double')
             normalizer = Normalizer()
             X = normalizer.fit_transform(vectorizer.fit_transform(select(data,train)))
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
             classifier = LinearSVC(multi_class='ovr')
             classifier.fit(X,y)
                
             print 'Grid Searched and Trained classifier',' @ ',time.strftime("%H:%M:%S")
                
            #
            #    testingDensity[i] = computeDensity(vectorizer, select(examples,test))
             
             trainingAccuracy[i] = accuracy_score(y,classifier.predict(X)) # predict(classifier,select(examples,train), labels[train], vectorizer, normalizer)
             print 'Training Accuracy',trainingAccuracy[i]
                
             testingAccuracy[i] = predict(classifier,select(data,test), labels[test],vectorizer,normalizer, i + 1, True)
             print 'Test Accuracy',testingAccuracy[i]
             testingF1[i] = predictF1(classifier,select(data,test), labels[test],vout,vectorizer,normalizer)
             print 'Test f1',testingF1[i]
             print 'Iteration '+str(i)+' done'
             fout.write('Iteration '+str(i)+' done'+'\n')
             vout.close()
             if testingF1[i]  >fmax: 
                 fmax=testingF1[i]
                 cmax=classifier
                 vmax=vectorizer
                 nmax=normalizer
        print "FINAL RESULTS:"+ parent+"\n"
        print "Training Accuracy:" + prettyPrint(trainingAccuracy)
        print "Test Accuracy:" + prettyPrint(testingAccuracy)
        print "Testing F1:" + prettyPrint(testingF1)
        print ' @ '+time.strftime("%H:%M:%S")
        fout.write("\n\nFINAL RESULTS "+parent+" :\n")    
        fout.write("Training Accuracy:" + prettyPrint(trainingAccuracy)+'\n')
        fout.write("Test Accuracy:" + prettyPrint(testingAccuracy)+'\n')
        fout.write("Testing F1:" + prettyPrint(testingF1)+'\n')
    
        print '\nBest Classifier for '+parent+' : '
        print cmax  
        fout.write('\nBest Classifier for '+parent+' : \n')  
        fout.write(str(cmax))
        
        #SAVING NEW CLASSIFIER
        pickle.dump(cmax,open('level'+str(level)+'/'+domain+'_'+parent+'_CMAX.p','wb'))
        pickle.dump(vmax,open('level'+str(level)+'/'+domain+'_'+parent+'_VMAX.p','wb'))
        pickle.dump(nmax,open('level'+str(level)+'/'+domain+'_'+parent+'_NMAX.p','wb'))

        fout.write('\n'+parent+'   SUCCESS!!!!!!!\n\n')
        print parent, ' SUCCESS!!!'
        fout.close()
        pout.write('1')
        pout.close()
        return True
    return True


def retrain(Param):
    data=Param[0]
    level = Param[1]
    parent = Param[2]

    print 'Retraining', parent
    try:
        labelDict=pickle.load(open('level'+str(level)+'/'+sd+'_'+parent+'_LABEL_DICT.p'))
        catMap=pickle.load(open('level'+str(level)+'/'+sd+'_'+parent+'_CAT_MAP.p'))
        labelMap=pickle.load(open('level'+str(level)+'/'+sd+'_'+parent+'_LABEL_MAP.p'))
        Rdata=pickle.load(open('level'+str(level)+'/DATA_'+sd+'_'+parent+'.p'))
    except:
        return
    try:    
        for d in data:
            Rdata.append(d)
    except(AttributeError):
        Rdata=[Rdata]
        for d in data:
            Rdata.append(d)
        
    pickle.dump(Rdata,open('level'+str(level)+'/DATA_'+sd+'_'+parent+'.p','wb'))
    
    
    
    currLabel=max(labelMap)+1
    hdata=[]
    for d in Rdata:
        if not catMap.has_key(d[1]):
            hdata.append(d)
            label=currLabel
            currLabel+=1
            labelDict[label]=len(d[0])
            catMap[d[1]]=label
            labelMap[label]=d[1]
    pickle.dump(catMap,open('level'+str(level)+'/'+sd+'_'+parent+'_CAT_MAP.p','wb'))
    pickle.dump(labelDict,open('level'+str(level)+'/'+sd+'_'+parent+'_LABEL_DICT.p','wb'))
    pickle.dump(labelMap,open('level'+str(level)+'/'+sd+'_'+parent+'_LABEL_MAP.p','wb'))    
    data=[]
    labels=[]
    for d in Rdata:
        label=catMap[d[1]]
        for title in d[0]:
            data.append(title)
            labels.append(label)
    
    fnTrain(parent,level,data,labels)    
    print 'calling hc'
    
    
    for d in hdata:
        hclassify(d[0],d[1], level+1)

def hclassify(hdata, parent, level):
    print 'Starting Hierarchical classification for parent = ', parent,' at level = ', level
    crumbs=[]
    for d in hdata:
        crumbs.append(titleMap[d.strip().lower()])
    data, labels, childData=readData(hdata,crumbs, parent)
    print 'Data read'

    if len(data)==0 or len(list(set(labels)))==1:
        return
    success=fnTrain(parent,level,data,labels)
    if not success:
        return
    for child in childData:
        retData=(childData[child],child)
        pickle.dump(retData,open('level'+str(level)+'/DATA_'+sd+'_'+parent+'.p','wb'))
        hclassify(childData[child],child, level+1)


def readData(Titles, Crumbs, parent):
    
    childData={}
    catMap={}
    labelMap={}
    labelDict={}
    currLabel=1
    Data=[]
    Labels=[]
    for i in range(0,len(Crumbs)):
                title = Titles[i].strip().lower()
                crumb = Crumbs[i]
                if ">" in crumb:
                    parts = crumb.split('>')

                    if len(parts) <=level:
                        continue
                    category=parts[level].strip().lower()
                    if not childData.has_key(category):
                        childData[category]=[]
                    childData[category].append(title)

                    if catMap.has_key(category):
                        label=catMap[category]
                    else:

                        catMap[category]=currLabel
                        label=currLabel
                        currLabel+=1
                        labelMap[label]=category


                    if labelDict.has_key(label):
                        labelDict[label]+=1
                    else:
                        labelDict[label]=1
                    Data.append(title)
                    Labels.append(label)


#    pickle.dump(catMap,open('level'+str(level)+'/'+sd+'_'+parent+'_CAT_MAP.p','wb'))
#    pickle.dump(labelDict,open('level'+str(level)+'/'+sd+'_'+parent+'_LABEL_DICT.p','wb'))
#    pickle.dump(labelMap,open('level'+str(level)+'/'+sd+'_'+parent+'_LABEL_MAP.p','wb'))
#
    examples=[]
    labels=[]
    limit=20

    for j in range(len(Labels)):
            if labelDict[Labels[j]] >limit:
                examples.append(Data[j])
                labels.append(Labels[j])
    return examples,labels, childData



def mode(y,Z):
    H={}
    
    for i in range(len(y)):
        if not H.has_key(y[i]):
            H[y[i]]=0
            
        H[y[i]]+=1
        
    mx=y[0]
    for i in y:
        if H[i]>H[mx]:
            mx=i
    
    val=(H[mx]*1.0)/len(y)
    
    return mx,val

def loadObjects(parent,level,dom):
    try:
        clf=pickle.load(open('level'+str(level)+'/'+dom+'_'+parent+'_CMAX.p'))
        vec=pickle.load(open('level'+str(level)+'/'+dom+'_'+parent+'_VMAX.p'))
        norm=pickle.load(open('level'+str(level)+'/'+dom+'_'+parent+'_NMAX.p'))
        return vec,norm,clf
    except(IOError,OSError):
        return -1,-1,-1
    except(AttributeError):
        print parent

def findCat(cmap,label, parent):

    for c in cmap:
        if cmap[c]==label:
            return c
    return '%'




def loadData():
    m=0


    for i in range(len(Crumbs)) :
            parts=Crumbs[i].split(' > ')
            if len(parts) > m:
                m=len(parts)
                
                
###################################################                
#    for i in range(len(Crumbs)) :
#        if 'screen protectors' in Crumbs[i].lower():
#                print Crumbs[i]
#                break
####################################################            
    for level in range(m):
        Data.append({})
        Parent.append({})
        Map.append({})
        RData.append({})
        RData.append({})
        Scores.append({})
        
        
                
        
        for i in range(len(Crumbs)) :
            if '>' not in Crumbs[i]:
                continue
#            
###################################
#            if 'screen protectors' not in Crumbs[i].lower():
#                continue
####################################            
#            
            
            
            parts=Crumbs[i].split('>')
            if len(parts) <= level:
                continue
            cat=parts[level].strip().lower()
            if not Data[level].has_key(cat):
                Data[level][cat]=[]
                if level==0:
                    Parent[level][cat]=''
                else:
                    Parent[level][cat]=parts[level-1].strip().lower()
#            title=Titles[i].strip().lower()
#            title=title.translate(None,string.punctuation).translate(None,string.digits)
#            title=re.sub(' [a-zA-Z]| [a-zA-Z]',' ',title)
            Data[level][cat].append(Titles[i])
    return m     




def checkOutlier(conf,y,label):
    Z=[]
    points=0
    for i in range(len(conf)):
        s=conf[i]
        cnt=0
        
        if y[i]==label:
            points+=1
            
            if len(numpy.shape(s))!=0:
                
            
                for j in s:
                    if j>0:
                        cnt=1
                        break
        
        Z.append(cnt)
        
            
    valid=sum(Z)*1.0/points
    
    return valid
        
def checkDup(str1, str2):
    str1=str1.split()
    str2=str2.split()
    scores=[]
    for u in str1:
        if len(u)<=3:
            continue
        w1=wn.morphy(u)
        if w1==None:
            continue
        U=wn.synsets(w1)
        if len(U)==0:
            continue
        U=U[0]
        maxScore=0
        for v in str2:
            if len(v)<=3:
                continue
            w2=wn.morphy(v)
            if w2==None:
                continue
            V=wn.synsets(w2)
            if len(V)==0:
                continue
            V=V[0]
            score=U.path_similarity(V)
            if score>maxScore:
                maxScore=score
        
        scores.append(maxScore)
    
    for u in str2:
        if len(u)<=3:
            continue
        w1=wn.morphy(u)
        if w1==None:
            continue
        U=wn.synsets(w1)
        if len(U)==0:
            continue
        U=U[0]
        maxScore=0
        for v in str1:
            if len(v)<=3:
                continue
            w2=wn.morphy(v)  
            if w2==None:
                continue
            V=wn.synsets(w2)
            if len(V)==0:
                continue
            V=V[0]
            score=U.path_similarity(V)
            if score>maxScore:
                maxScore=score
        
        scores.append(maxScore)
            
    val=numpy.mean(scores)        
    if val>0.6:
        return True,val
    return False,val
    
def prediction(level1,level2,cat,parent,fout,rout,dom,M,direction):

    
    vec,norm,clf=loadObjects(parent,level2,dom)
    if vec==-1:
        
        return parent,-3
    try:    
        cmap=pickle.load(open('level'+str(level2)+'/'+dom+'_'+parent+'_CAT_MAP.p'))
    except (OSError,EnvironmentError):
        
        
        return '',-3
        
    
   
    if len(Data[level1][cat]) >= 50  :
        
#        print 'Insufficient data for ',cat,' size = ',len(Data[level1][cat])
#    else:
#            print "Matching ",cat, ' at ', level        
            X=norm.transform(vec.transform(Data[level1][cat]))
            y=clf.predict(X)
            C=clf.decision_function(X)
                
            Z=[]
            for i in range(len(y)):
                Z.append(abs(numpy.max(C[i])))   
            label,occ=mode(y,Z)
            
            newCat=findCat(cmap,label,parent)
            
            d=checkOutlier(C,y,label)
            if occ<=0.35:
                flag=True

            elif d<0.5:
                flag=True
            else:
                flag=False
            
            print(cat+'('+str(level1)+')\t'+newCat+'('+str(level2)+')\t'+'Score1 = '+ str(occ)+'\t'+' Score2 = '+str(d)+'('+str(flag)+')')
            fout.write(cat+','+str(level1)+','+newCat+','+str(level2)+','+'Score1 = '+ str(occ)+','+' Score2 = '+str(d)+'('+str(flag)+')'+'\n')
            
            if not flag:
                tmpScore=0.0
                if M[level1].has_key(cat):
                    tmpScore=M[level1][cat][2]
                if occ > tmpScore:
                    M[level1][cat]=(level2,newCat,occ,d)
                    Scores[level1][cat]=(occ,d)
                    return newCat,occ
                

            if not M[level1].has_key(cat) or (Scores[level1].has_key(cat) and (Scores[level1][cat][0]<0.4 and Scores[level1][cat][1]<0.6)):
                if not RData[level2].has_key(parent):
                    RData[level2][parent]=[]
                RData[level2][parent].append((Data[level1][cat],cat))
                for c in cmap:
                    flag,mscore=checkDup(c,cat)
                    if flag:
                        if c==newCat or mscore>0.8:
                            M[level1][cat]=(level2,newCat,occ)
                            Scores[level1][cat]=(occ,d)
                            return newCat,occ
                        else:
                            
                            print('-> '+cat +' duplicate of '+c+ ' Level= '+str(level2)+' Parent = '+parent)
                            Dup.append([level2,parent,cat,c])
                            break
                print '-> Category ' +cat+ ' Added to RData at ',level2,' to parent '+parent+'\n'
                rout.write('Category ' +cat+ ' Added to RData at '+str(level2)+' to parent '+parent+'\n')
                return '',-1
            else: 
                newCat=M[level1][cat][1]
                score=M[level1][cat][2]
                return newCat,score
    else:
        
        return '',-2
   
def parallelPredict(param,fout,rout): 
        cat=param[0]
        level=param[1]
        level2=0
        if level==0:
            par=(-1,'')
            
        else: 
#            print 'Reached ', cat
            tmp=Parent[level][cat]
            
                
            if not Map[level-1].has_key(tmp):
                
                return '',-4
                
            else:
                
                par=Map[level-1][tmp]
                level2=par[0]+1
#                print 'Cat = ',cat,'Orig Parent =',Parent[level][cat],'New Par = ',par
     
#        print level,'---',level2
        newCat,score=prediction(level,level2,cat,par[1],fout,rout,sd,Map,1)
#        if level==1:
#            print 'newCat = ',newCat, ' score = ',score
        if score<0:
#            print 'return value  ',score, ' for ', cat
            return '',score
            
        score2=1
        i=1
        while score >0:
            
            newCat2,score2=prediction(level,level2+i,cat,newCat,fout,rout,sd,Map,1)
            
            if score2<=score:
                
                break
            else:
                score=score2
                newCat=newCat2
                
                i+=1
        print '-> ',cat,' mapped to ',newCat
        return newCat,level2+i
                

sd=(sys.argv[1])
td=sys.argv[2]
if sd=='amazon':
    print 'Warning: Trying to modify actual data'
level=0
parent=''

#for each level

Crumbs=pickle.load(open('Data/'+td+'_CRUMBS.p'))
Titles=pickle.load(open('Data/'+td+'_TITLES.p'))

if len(Crumbs)!=len(Titles):
    print 'Data Corrupted' 
    exit
if len(Crumbs) > 1000000:
    Crumbs=Crumbs[1:1000000]
    Titles=Titles[1:1000000]

titleMap={}
for i in range(len(Titles)):
    if '>' in Crumbs[i]:
        t=Titles[i].strip().lower()
        if not titleMap.has_key(t):
            titleMap[t]=Crumbs[i]

maxLevels=loadData()
currLevel=-1
print 'Data Loaded..'
nproc=int(sys.argv[3])
pool=Pool(processes=nproc)
start=time.time()
Mapped={}
MCounts=[]
end=False
for level in range(maxLevels):
    MCounts.append([0,0,0])
    fout=open('TaxonomyAlignment/reports/MatchingReports/'+sd+'_'+td+'_MatchReport'+str(level)+'.csv','wb')
    rout=open('TaxonomyAlignment/reports/MatchingReports/'+sd+'_'+td+'_Retraining'+str(level)+'.txt','wb')
    vout=open('TaxonomyAlignment/reports/MatchingReports/'+sd+'_'+td+'_MatchVerifyReport'+str(level)+'.txt','wb')
    Cats= []
    for cat in Data[level]:
        Cats.append((cat,level))
    print 'Starting predictions for level ',level
    
    
    eout=open('TaxonomyAlignment/reports/MatchingReports/'+sd+'_'+td+'_FailureReport'+str(level)+'.csv','wb')
    for c in Cats:
            ####################
            # FORWARD MAPPING

            vCat,vLevel=parallelPredict(c,fout,rout)
#            vLevel+=1
            cat=c[0]
            
            if vLevel==-1:
                eout.write('No forward mapping for '+cat+'\n')
                MCounts[level][2]+=1
                continue
            if vLevel==-2:
                eout.write('Insufficient Data to make a mapping for cat:'+cat+'\n') 
#                MCounts[level][2]+=1
                continue
            if vLevel==-3:
                eout.write('Reached Leaf '+parent+'\n')
#                MCounts[level][2]+=1
                continue
            if vLevel==-4:
                eout.write('Parent '+Parent[level][cat]+' not trained for '+cat+'\n')
#                print('Parent '+Parent[level][cat]+' not trained for '+cat)
                continue
            ######### 
            # REVERSE MAPPING
    
            
            
            try:
                vData=pickle.load(open('level'+str(vLevel)+'/DATA_'+sd+'_'+vCat+'.p'))
            except:
                print 'Data not found for cat ', vCat, ' at ', vLevel
                MCounts[level][1]+=1
                eout.write('Data not found for reverse mapping for '+ vCat+ ' at '+ str(vLevel)+'\n')
                continue
                
            data=[]
            for d in vData:
                for t in d[0]:
                    t=t.translate(None,string.punctuation).translate(None,string.digits)
                    data.append(t) 
            par=Parent[level][cat]
            vec,norm,clf=loadObjects(par,level,td)
#            print 'here',vec,par, len(data)
            if vec==-1:
                eout.write('Src objects not found for reverse mapping for '+cat+' - child of '+par+'\n')
                print('Src objects not found for reverse mapping for '+cat+' - child of '+par)
                MCounts[level][1]+=1
#                print('Parent '+Parent[level][cat]+' not trained for '+cat)
                continue
                
            try:
                x=norm.transform(vec.transform(data))
            except:
                print 'Data not found for cat ', vCat, ' at ', vLevel
                MCounts[level][1]+=1
                eout.write('Data not found for reverse mapping for '+ vCat+ ' at '+ str(vLevel)+'\n')
                continue
            y=clf.predict(x)
            C=clf.decision_function(x)
            Z=[]
            for i in range(len(y)):
                Z.append(abs(numpy.max(C[i])))   
            label,occ=mode(y,Z)
            cmap=pickle.load(open('level'+str(level)+'/'+td+'_'+par+'_CAT_MAP.p'))
            newCat=findCat(cmap,label,par)
#            print newCat,occ,'\n'
            if Map[level].has_key(cat):
                print '-> ',cat,' to ',Map[level][cat][1],' to ',newCat
                vout.write(cat+' | '+Map[level][cat][1]+' | '+newCat+'\n')
                if cat==newCat:
                    MCounts[level][0]+=1
                else:
                    MCounts[level][1]+=1
            
    
    fout.close()    
    vout.close()
    rout.close()
    eout.close()
    
    
print '\n\nCounts:'
print '2-way','\t','1-way','\t','no match'
cout=open('TaxonomyAlignment/reports/MatchingReports/'+sd+'_'+td+'_Counts.csv','wb')
cout.write('2-way,1-way,no match'+'\n')
for level in range(len(MCounts)):
    for j in range(3):
        print MCounts[level][j],'\t',
    print ''
    cout.write(str(MCounts[level][0])+','+str(MCounts[level][1])+','+str(MCounts[level][2])+'\n')
cout.close()

    
    
    
    
    
    # Pr=pool.map(parallelPredict,Cats)

for level in range(maxLevels):

    for cat in Map[level]:
        newCat=Map[level][cat][1]
        newLevel=Map[level][cat][0]
        newKey=(newLevel,newCat)
        if Mapped.has_key(newKey):
            count=Mapped[newKey][0]
            catInfo=Mapped[newKey][1]
            count+=1
            catInfo.append((level,cat))
            Mapped[newKey]=[count,catInfo]


        else:
            Mapped[newKey]=[1,[(level,cat)]]
            
            

            
            
rout=open('TaxonomyAlignment/reports/'+td+'_Demotions.txt','wb')  

for item in Mapped:
     newKey=item
     newCat=newKey[1]
     newLevel=newKey[0]
     if Mapped[item][0]>1:
         temp=Mapped[item][1]
         Mapped[item][0]=0
         for tempItem in temp:
             cat=tempItem[1]
             level=tempItem[0]
             Map[level].pop(cat)
             if len(RData) <= newLevel+1:
                 RData.append({})
             if not RData[newLevel+1].has_key(newCat):
                     RData[newLevel+1][newCat]=[]
             RData[newLevel+1][newCat].append((Data[level][cat],cat))
             print 'Category ' +cat+ ' Added to RData at ',(newLevel+1),' to parent '+newCat+' \n'
             rout.write('Category ' +cat+ ' Added to RData at '+str(newLevel+1)+' to parent '+newCat+' \n')
rout.close()

for level in range(maxLevels):
     Params=[]

     for p in RData[level]:
         Params.append((RData[level][p],level,p))
     print 'Retraining loop', len(Params), level

     # B=pool.map(retrain,Params)
     for p in Params:
         B=retrain(p)

pickle.dump(Map,open('MAP_'+sd+'_'+td+'.p','wb'))
dout=open('TaxonomyAlignment/reports/'+td+'_Duplicates.txt','wb')
print 'Duplicates'
for d in Dup:

     for f in d:

         dout.write(str(f)+',')
     print d
     dout.write('\n')
dout.close()

for level in range(maxLevels):
     print 'Scores for level ',level
     Scores.append({})
     for cat in Map[level]:
         flag,Scores[level][cat]=checkDup(cat,Map[level][cat][1])
         print cat,' = ',Scores[level][cat]
print 'Time taken = ',(time.time()-start), ' s'