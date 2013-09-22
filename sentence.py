import bktree
import phrase
import math
import ngram_pos
import urllib2
import re
if __name__ == "__main__":
    tree = bktree.BKTree(bktree.damerau_levenshtein_distance,
                  bktree.dict_words('/usr/share/dict/american-english'))
    vocabulary = []
    iterator = bktree.dict_words('/usr/share/dict/american-english')
    for i in iterator:
        vocabulary.append(i)
    postagged = ngram_pos.getcounts_tagged('/home/akhilesh/Desktop/NLP/Assignments/nlp/tagged2.txt')
    dist = 2
    while True:
        
        print "Press 0 to exit"
        print "Press 1 for just single word errors"
        print "Press 2 or 3 to test for phrases"
        
        num = str(raw_input("Please enter the number : "))
        if num == '0':
            break
        if num == '1':
            i = str(raw_input("Enter the word : "))
            i = i.lower()
            i = re.sub('[.,"<>?/\|{~`]', ' ', i)
            edit_0 = [];
            edit_1 = [];
            edit_2 = [];
            if i not in vocabulary:
                w = set(tree.query(i, dist)) - set([i]) #Candidates!
                max_val = 0;
                max_candidate = 0
                for pair in w:
                    #print i + " : " + pair[1]
                    if pair[0] == 0:
                        edit_0.append(pair[1])
                    elif pair[0] == 1:
                        edit_1.append(pair[1])
                    else: 
                        edit_2.append(pair[1])
                    ed = bktree.get_edits(i, pair[1])
                    if(bktree.Pedit(ed) > max_val):
                        max_val = bktree.Pedit(ed)
                        max_candidate = pair[1]
                print "The most likely replacement for " + i + " is : " + str(max_candidate)
        
        if num == '2' or num == '3':
            i = str(raw_input("Enter the sentence : "))
            i = i.lower()
            i = re.sub('[.,"<>?/\|{~`]', ' ', i)
            log_prob_ngrams = []
            words = i.split()
            for j in xrange(len(words)):
                word = words[j]
                edit_0 = [];
                edit_1 = [];
                edit_2 = [];
                score_edits = []
                if word not in vocabulary:
                    w = set(tree.query(word, dist)) - set([word]) #Candidates!
                    max_val = 0;
                    max_candidate = 0
                    for pair in w:
                        #print i + " : " + pair[1]
                        if pair[0] == 0:
                            edit_0.append(pair[1])
                        elif pair[0] == 1:
                            edit_1.append(pair[1])
                        else: 
                            edit_2.append(pair[1])
                        ed = bktree.get_edits(i, pair[1])
                        score_edits.append(bktree.Pedit(ed))

                    score_post = ngram_pos.choose(' '.join(words[:j-1]), edit_1 ,' '.join(words[j+1:]),postagged)
                    log_score_post = [math.log(score) for score in score_post]
                    log_prob_ngrams = [phrase.get_prior(' '.join(words[:j-1])+' '+ candidate + ' ' + ' '.join(words[j+1:])) for candidate in edit_1 ]
                    final_scores = []
                    weight_post = 0.25
                    weight_ngrams = 0.75
                    for k in xrange(len(edit_1)):
                        final_scores.append(weight_post*log_score_post[k] +
                                weight_ngrams*log_prob_ngrams[k] +
                                math.log(score_edits[k]))
                        #print str(edit_1[k]) + ' --- ' + str(final_scores[k])
                    res=[(edit_1[i],final_scores[i]) for i in xrange(len(edit_1))]
                    res.sort(key=lambda par:-par[1])
                    print res
