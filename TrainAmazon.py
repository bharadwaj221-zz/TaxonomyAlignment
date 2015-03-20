# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 19:27:33 2015

@author: bharadwaj
"""

import os,sys
n=(sys.argv[1])
os.system('rm level0/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 0 amazon '+n+' 1000 10000')

os.system('rm level1/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 1 amazon '+n+' 500 5000')

os.system('rm level2/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 2 amazon '+n+' 200 1000')

os.system('rm level3/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 3 amazon '+n+' 100 500')

os.system('rm level4/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 4 amazon '+n+' 20 100')

os.system('rm level5/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 5 amazon '+n+' 20 50')


os.system('rm level6/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 6 amazon '+n+' 20 50')


os.system('rm level7/STATUS/*')
os.system('python2.7 TaxonomyAlignment/TrainMP.py 7 amazon '+n+' 20 50')