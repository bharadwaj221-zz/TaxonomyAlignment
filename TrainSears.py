# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 19:27:33 2015

@author: bharadwaj
"""

import os,sys
n=(sys.argv[1])
os.system('rm level0/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 0 sears '+n+' 1000 1000')

os.system('rm level1/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 1 sears '+n+' 1000 5000')

os.system('rm level2/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 2 sears '+n+' 500 5000')

os.system('rm level3/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 3 sears '+n+' 200 2000')

os.system('rm level4/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 4 sears '+n+' 100 1000')

os.system('rm level5/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 5 sears '+n+' 50 500')


os.system('rm level6/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 6 sears '+n+' 20 250')


os.system('rm level7/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 7 sears '+n+' 10 100')