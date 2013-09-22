from nltk.tag.stanford import POSTagger
from nltk import sent_tokenize, word_tokenize
from collections import defaultdict
import pickle
import string
import re

st = POSTagger( '/home/akhilesh/Desktop/NLP/Assignments/nlp/stanford-postagger-full-2013-06-20/models/english-left3words-distsim.tagger',
        '/home/akhilesh/Desktop/NLP/Assignments/nlp/stanford-postagger-full-2013-06-20/stanford-postagger-3.2.0.jar')

#st = POSTagger(
#'/home/chinmay/scratch/stanford-postagger-full-2013-06-20/models/english-left3words-distsim.tagger',
#'/home/chinmay/scratch/stanford-postagger-full-2013-06-20/stanford-postagger-3.2.0.jar')

def getcounts(corpname,data=defaultdict(int)):
    f=open(corpname)
    text = f.read().lower()
    #data = defaultdict(int)
    print 'Start tokenize'
    sents = [word_tokenize(sent) for sent in sent_tokenize(text)]
    print 'Start tagging'
    tagged = st.batch_tag(sents)

    for sent in tagged:
        for i in xrange(len(sent)-2):
            data[( sent[i][1],sent[i+1][1],sent[i+2][1] )] += 1

            data[( sent[i][0],sent[i+1][1],sent[i+2][1] )] += 1
            data[( sent[i][1],sent[i+1][0],sent[i+2][1] )] += 1
            data[( sent[i][1],sent[i+1][1],sent[i+2][0] )] += 1

    return data


def choose(leftcont,confusion,rightcont,data):
    leftwords = word_tokenize(leftcont)
    rightwords = word_tokenize(rightcont)
    loc = len(leftwords)
    scores = [1]*len(confusion)
    for k in xrange(len(confusion)):
        tagged = st.tag(leftwords+[confusion[k]]+rightwords)
        sent = [tagged[i][1] for i in xrange(loc)] + [tagged[loc][0]] + \
            [tagged[i][1] for i in xrange(loc+1,len(tagged))]
        for j in xrange(len(sent)-2):
            trigram = (sent[j],sent[j+1],sent[j+2])
            sc = data[trigram]
            scores[k] *= (sc + 1)
        for j in xrange(1,len(sent)-2):
            bigram = (sent[j],sent[j+1])
            sc = data[bigram]
            scores[k] /= float(sc+1)
    return scores



def getcounts_tagged(corpname,data=defaultdict(int)):
    f=open(corpname)
    for line in f:
        sent = [x.split('_') for x in line.strip().split()]
        for i in xrange(len(sent)-2):
            data[( sent[i][1],sent[i+1][1],sent[i+2][1] )] += 1

            data[( sent[i][0],sent[i+1][1],sent[i+2][1] )] += 1
            data[( sent[i][1],sent[i+1][0],sent[i+2][1] )] += 1
            data[( sent[i][1],sent[i+1][1],sent[i+2][0] )] += 1

        for i in xrange(len(sent)-1):
            data[( sent[i][1],sent[i+1][1] )] += 1

            data[( sent[i][1],sent[i+1][0] )] += 1
            data[( sent[i][0],sent[i+1][1] )] += 1

    return data
