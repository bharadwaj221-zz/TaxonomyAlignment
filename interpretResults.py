# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 11:26:14 2014

@author: bharadwaj
"""
import pickle, sys
fin=open(sys.argv[1])
domain=sys.argv[2]
fout=open('TaxonomyAlignment/reports/'+domain+'_catResults.txt','wb')
cat='###'
catMap=pickle.load(open(domain+'_CAT_MAP.p'))
for line in fin:
    parts=line.split()
    #print len(parts)
    if len(parts)==5:
        #print parts
        label=parts[0].strip()
        for j in catMap:
            if catMap[j]==int(label):
                cat=j
                break
        print cat+':'+parts[1].strip()+':'+parts[2].strip()+':'+parts[3].strip()+':'+parts[4].strip()
        fout.write(cat+':'+parts[1].strip()+':'+parts[2].strip()+':'+parts[3].strip()+':'+parts[4].strip()+':'+'\n')
fin.close()
fout.close()