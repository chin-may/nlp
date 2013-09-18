from collections import defaultdict
import pickle
import string
import re
from lxml import etree

def getcounts(corp,dictwords,k,picklename):
    words = corp.read().translate(string.maketrans('',''),string.punctuation).split()
    #data = pickle.load(open(picklename,'rb'))
    data = defaultdict(int)
    #pickle.dump(data, open(picklename+'_old','wb'))
    for i in xrange(len(words) - k):
        word = words[i].lower()
        if word not in dictwords:
            continue
        for j in xrange(k):
            contextword = words[i+j+1].lower()
            if contextword not in dictwords:
                continue
            data[(max(word,contextword), min(word,contextword))] += 1
    pickle.dump(data, open(picklename,'wb'))
    return data

f = open('/usr/share/dict/cracklib-small')
dct = set(f.read().lower().split())

def choose(confusion, context,data):
    scores = [0]*len(confusion)
    for i in xrange(len(context)):
        tscore = [0]*len(confusion)
        currsum = 0
        for j in xrange(len(confusion)):
            tscore[j] = data[(max(context[i],confusion[j]),min(context[i],confusion[j]))]
            currsum += tscore[j]
        if currsum is not 0:
            for j in xrange(len(confusion)):
                scores[j] += tscore[j]/float(currsum)
    return scores

def read_br():
    txt=etree.tostring(etree.parse('/home/chinmay/scratch/brown_tei/Corpus.xml'),encoding='utf8',method='text')
    txt = re.sub(r'[\n\t]','',txt)
    f=open('stripped_brown','w')
    f.write(txt)
    f.close()

