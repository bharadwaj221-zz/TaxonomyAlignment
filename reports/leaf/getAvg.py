# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 15:29:39 2014

@author: bharadwaj
"""
import sys
# ls -1 report_*_2.txt >reportFiles.txt

fin=open('reportFiles.txt')
avg=0.0
A=[]
for line in fin:
    rep=open(line.strip())
    total=0.0
    count=0
    for l in rep:    
        
        parts=l.split()
        if len(parts)==5:
            total+=(float(parts[3].strip()))
            count+=1
            
    rep.close()
    avg=total/(1.0*count)
    A.append(avg)
print sum(A)/(len(A)*1.0)
        