# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 13:40:55 2014

@author: bharadwaj
"""
import os
import time
import sys
import pickle
### PARALLEL
k=(sys.argv[2])
domain=sys.argv[1]
limit=sys.argv[3]
if k=='0':
    parents=['']
else:    
    parents=pickle.load(open('level'+k+'/'+domain+'_Level'+str(int(k)-1)+'_Categories.p'))
n=len(parents)

start = time.time()

os.system('seq '+str(n)+' | parallel -j 8 python2.7 TaxonomyAlignment/TrainMT.py amazon '+k+' '+limit) 
end = time.time()
print 'Time = ',str((end-start)),' s'
pout=open('level'+k+'/TIME_STATUS.txt','wb')
pout.write('Time = '+str((end-start))+' s')
pout.close()


### SERIAL

#
#start = time.time()
#for k in xrange(1):
#    for i in xrange(100):
#        os.system('python2.7 level2/LevelTwoTrainMT.py amazon '+str(i+1)) 
#        
#end = time.time()
#print 'Time = ',str((end-start)/2),' s'
