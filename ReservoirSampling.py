import random, sys, pickle

 
# Force the value of the seed so the results are repeatable
random.seed(12345)
domain=sys.argv[1]
sample_titles = []
SAMPLE_COUNT = int(sys.argv[2])
Titles=pickle.load(open('Data/'+domain+'_FULL_TITLES.p'))
Crumbs=pickle.load(open('Data/'+domain+'_FULL_CRUMBS.p'))
cmap={}
for i in range(len(Crumbs)):
    if not cmap.has_key(Crumbs[i]):
        cmap[Crumbs[i]]=[]
    cmap[Crumbs[i]].append(Titles[i])
titles=[]
crumbs=[]
print 'Total crumbs = ',len(cmap)
for crumb in cmap:        
    sample_titles=[]
    for index,title in enumerate(cmap[crumb]):
            # Generate the reservoir
            if index < SAMPLE_COUNT:
                    sample_titles.append(title)
            else:
                    # Randomly replace elements in the reservoir
                    # with a decreasing probability.
                    # Choose an integer between 0 and index (inclusive)
                    r = random.randint(0, index)
                    if r < SAMPLE_COUNT:
                            sample_titles[r] = title
    cmap[crumb]=sample_titles
    for t in sample_titles:
        titles.append(t)
        crumbs.append(crumb)
    
pickle.dump(crumbs,open('Data/'+domain+'_CRUMBS.p','wb'))
pickle.dump(titles,open('Data/'+domain+'_TITLES.p','wb'))