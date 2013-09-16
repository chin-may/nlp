from collections import defaultdict
import pickle
def getcounts(corp,dictwords,k,picklename):
    words = corp.read().split()
    data = pickle.load(open(picklename,'rb'))
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

f = open('/usr/share/dict/words')
dct = set(f.read().lower().split())
