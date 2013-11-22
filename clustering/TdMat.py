import textmining
from nltk.corpus import brown
import nltk.data
import nltk
from pprint import pprint

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
tdm = textmining.TermDocumentMatrix()


def print_tdm():
    for row in tdm.rows(cutoff=1):
        print row

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    return [' '.join(l[i:i+n]) for i in range(0, len(l), n)]

def process_sample(sample):
    """
    Input - A file id containing the sample - e.g. cr02

    Tokenizes the document into sentences.
    Groups K sentences at a time.

    Output - A List of List of sentences. Each inner list has K sentences.
             Each outer list corresponds to one document.
    """
    K = 20
    words_in_sample = brown.words(sample)
    temp_str = ' '.join(words_in_sample)

    sentences = sent_tokenizer.tokenize(temp_str)
    return  chunks(sentences,K)


def split(fname,numrows):
    f=open(fname)
    i=0
    j=1
    wf = open(fname+'_p0','w')
    f.readline()
    for line in f:
        if i==numrows:
            wf.close()
            wf = open(fname+'_p'+str(j),'w')
            i=0
            print j
            j+=1
        wf.write(line+'\n')
        i+=1
    wf.close()

#Tests

#print_tdm()
#print len(docs)


#pprint(docs)

