import nltk
import sys
from nltk.corpus import semcor
from nltk.corpus import wordnet as wn
import glob
import os
os.chdir("/home/akhilesh/nltk_data/corpora/semcor/brown1/tagfiles/")


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return ''

for files in glob.glob("*.xml"):
    print files
    outfile =  open("/home/akhilesh/Desktop/NLP/Project/synsetTaggedSemCor/brown1/"+ str(files.split('.')[0]), "w")
    sentences = semcor.xml('brown1/tagfiles/' + files).findall('context/p/s')
    i = 0
    for sent in sentences:
        i+=1
        for wordform in sent.getchildren():
            hasWNSN = False
            hasPOS = False
            wnsn = 0
            if len(wordform.text)  > 0:
                for key in sorted(wordform.keys()):
                    if key=='pos':
                        hasPOS=True
                    elif key=='wnsn':
                        hasWNSN=True
                        stringWNSN = wordform.get('wnsn').split(';')
                        #print wordform.text + "===" + wordform.get('pos') +"===" + wordform.get('wnsn') + wordform.get('lemma'),
                        wnsn = int(stringWNSN[0])
                    #else:
                    #    print(key+ "="+ str(wordform.get(key)))
                if hasWNSN and hasPOS:
                    if wnsn > 0: #and wordform.get('pos')[0] != 'J':
                        #if wnsn < len(wn.synsets(wordform.text)):
                        outfile.write('SynsetID'+
                                str(wn.synsets(wordform.get('lemma'), get_wordnet_pos(wordform.get('pos')))[wnsn-1].offset) + ' ')
                        #else :
                        #    outfile.write('SynsetID'+
                        #        str(wn.synsets(wordform.text)[0].offset) + ' ')
                    else:
                        outfile.write(wordform.text + ' ')
                elif hasPOS:
                    outfile.write(wordform.text + ' ')
        outfile.write("\n")
    outfile.close()

