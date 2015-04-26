# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 14:32:32 2014

@author: bharadwaj
"""
import sys,os,re


domain=sys.argv[1]
scores=[]
fout = open("TaxonomyAlignment/"+domain+"_ConsolidatedResults.txt",'wb')
for level in range(8):
    scores=[]
    flag=False
    fout.write('Level '+str(level)+'\n')
    path='TaxonomyAlignment/reports/level'+str(level)
#    flist=os.system('ls -1 '+path+'/'+domain+'_Level_*_Results* ')
    flist=os.listdir(path+'/')
#    flist=open(path+'/ResultFiles')
    score=0
    for line in flist:
        re.match
        if domain not in line or 'Level' not in line or 'Results' not in line:
            continue
        flag=True
        cat=line.split('_')[4].split('.')[0]
        line=line.split('\n')[0]
        fin=open(path+'/'+line)
        for i, l in enumerate(fin):
            if 'Testing F1' in l:
                
                score = l.split(':')[1].split('(')[0]
                
                #print cat,'---', score
                fout.write(cat+":"+str(score)+'\n')
                scores.append(float(score))
        fin.close()
    try:    
        print 'Level ',level,': Avg F1 = ',sum(scores)/(1.0*len(scores)), flag
    except:
        print 'NA'
    
#    flist.close()
fout.close()        




#Iteration no 0 @ 06:44:09
#Iteration 0 done
#Iteration no 1 @ 06:47:40
#Iteration 1 done
#Iteration no 2 @ 06:51:20
#Iteration 2 done
#
#
#FINAL RESULTS industrial  scientific :
#Training Accuracy:0.9533(0.0002)
#Test Accuracy:0.8909(0.0007)
#Testing F1:0.8900(0.0007)
            
