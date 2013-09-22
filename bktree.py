"""

This module implements Burkhard-Keller Trees (bk-tree).  bk-trees
allow fast lookup of words that lie within a specified distance of a
query word.  For example, this might be used by a spell checker to
find near matches to a mispelled word.

The implementation is based on the description in this article:

http://blog.notdot.net/2007/4/Damn-Cool-Algorithms-Part-1-BK-Trees

Licensed under the PSF license: http://www.python.org/psf/license/

- Adam Hupp <adam@hupp.org>

"""
from itertools import imap, ifilter
import collections
import random, operator

class BKTree:
    def __init__(self, distfn, words):
        """
        Create a new BK-tree from the given distance function and
        words.
        
        Arguments:

        distfn: a binary function that returns the distance between
        two words.  Return value is a non-negative integer.  the
        distance function must be a metric space.
        
        words: an iterable.  produces values that can be passed to
        distfn
        
        """
        self.distfn = distfn

        it = iter(words)
        root = it.next()
        self.tree = (root, {})

        for i in it:
            self._add_word(self.tree, i)

    def _add_word(self, parent, word):
        pword, children = parent
        d = self.distfn(word, pword)
        if d in children:
            self._add_word(children[d], word)
        else:
            children[d] = (word, {})

    def query(self, word, n):
        """
        Return all words in the tree that are within a distance of `n'
        from `word`.  

        Arguments:
        
        word: a word to query on

        n: a non-negative integer that specifies the allowed distance
        from the query word.  
        
        Return value is a list of tuples (distance, word), sorted in
        ascending order of distance.
        
        """
        def rec(parent):
            pword, children = parent
            d = self.distfn(word, pword)
            results = []
            if d <= n:
                results.append( (d, pword) )
                
            for i in range(d-n, d+n+1):
                child = children.get(i)
                if child is not None:
                    results.extend(rec(child))
            return results

        # sort by distance
        return sorted(rec(self.tree))
    


def brute_query(word, words, distfn, n):
    """A brute force distance query

    Arguments:

    word: the word to query for

    words: a iterable that produces words to test

    distfn: a binary function that returns the distance between a
    `word' and an item in `words'.

    n: an integer that specifies the distance of a matching word
    
    """
    return [i for i in words
            if distfn(i, word) <= n]

def maxdepth(tree, count=0):
    _, children = t
    if len(children):
        return max(maxdepth(i, c+1) for i in children.values())
    else:
        return c


def levenshtein(s, t):
    m, n = len(s), len(t)
    d = [range(n+1)]
    d += [[i] for i in range(1,m+1)]
    for i in range(0,m):
        for j in range(0,n):
            cost = 1
            if s[i] == t[j]: cost = 0

            d[i+1].append( min(d[i][j+1]+1, # deletion
                               d[i+1][j]+1, #insertion
                               d[i][j]+cost) #substitution
                           )
    return d[m][n]

def product(nums):
    "Return the product of a sequence of numbers."
    return reduce(operator.mul, nums, 1)

class Pdist(dict):
    "A probability distribution estimated from counts in datafile."
    def __init__(self, data=[], N=None, missingfn=None):
        for key,count in data:
            self[key] = self.get(key, 0) + int(count)
        self.N = float(N or sum(self.itervalues()))
        self.missingfn = missingfn or (lambda k, N: 1./N)
        print self.N
        print count
    def __call__(self, key): 
        if key in self: return self[key]/self.N  
        else: return self.missingfn(key, self.N)

def datafile(name, sep='\t'):
    "Read key,value pairs from file."
    for line in file(name):
        yield line.split(sep)

def avoid_long_words(key, N):
    "Estimate the probability of an unknown word."
    return 10./(N * 10**len(key))

N = 1024908267229 ## Number of tokens

def Pedit(edit):
    "The probability of an edit; can be '' or 'a|b' or 'a|b+c|d'." 
    if edit == '': return (1. - p_spell_error) 
    return p_spell_error*product(P1edit(e) for e in edit.split('+')) 

p_spell_error = 1./20. 

P1edit = Pdist(datafile('count_1edit.txt')) ## Probabilities of single edits 

def damerau_levenshtein_distance(a, b):
	INF = len(a) + len(b)
	matrix = [[INF for n in xrange(len(b) + 2)]]
	matrix += [[INF] + range(len(b) + 1)]
	matrix += [[INF, m] + [0] * len(b) for m in xrange(1, len(a) + 1)]
	last_row = {}
	for row in xrange(1, len(a) + 1):
		ch_a = a[row-1]
		last_match_col = 0
		for col in xrange(1, len(b) + 1):
			ch_b = b[col-1]
			last_matching_row = last_row.get(ch_b, 0)
			cost = 0 if ch_a == ch_b else 1
			matrix[row+1][col+1] = min(
				matrix[row][col] + cost, # Substitution
				matrix[row+1][col] + 1,  # Addition
				matrix[row][col+1] + 1,  # Deletion
				# Transposition
				matrix[last_matching_row][last_match_col]
					+ (row - last_matching_row - 1) + 1
					+ (col - last_match_col - 1))
			if cost == 0:
				last_match_col = col
		last_row[ch_a] = row
	return matrix[-1][-1]

def get_edits(a, b):
	INF = len(a) + len(b)
	matrix = [[INF for n in xrange(len(b) + 2)]]
	matrix += [[INF] + range(len(b) + 1)]
	matrix += [[INF, m] + [0] * len(b) for m in xrange(1, len(a) + 1)]
	operation = [['' for n in xrange(len(b) + 2)] for m in xrange(len(a) + 2)]
	last_row = {}
	final_operations = []
	final_edits = ''
	for row in xrange(1, len(a) + 1):
		ch_a = a[row-1]
		last_match_col = 0
		for col in xrange(1, len(b) + 1):
			ch_b = b[col-1]
			last_matching_row = last_row.get(ch_b, 0)
			cost = 0 if ch_a == ch_b else 1
			matrix[row+1][col+1] = min(
				matrix[row][col] + cost, # Substitution
				matrix[row+1][col] + 1,  # Addition
				matrix[row][col+1] + 1,  # Deletion
				# Transposition
				matrix[last_matching_row][last_match_col]
					+ (row - last_matching_row - 1) + 1
					+ (col - last_match_col - 1))
			if matrix[row+1][col+1] == matrix[row][col]+cost:
				operation[row+1][col+1] = ('S', row, col, cost, row+1, col+1)
			elif matrix[row+1][col+1] == matrix[row+1][col] + 1:
			    operation[row+1][col+1] = ('A', row + 1, col, 1, row+1, col+1)
			elif matrix[row+1][col+1] == matrix[row][col+1] + 1:
			    operation[row+1][col+1] = ('D', row, col + 1, 1, row+1, col+1)
			else:
			    operation[row+1][col+1] = ('T', last_matching_row, last_match_col, 1, row, col+1)
			    
			if cost == 0:
				last_match_col = col
		last_row[ch_a] = row
	row = len(a) + 1
	col = len(b) + 1
	row1 = row
	col1 = col
	while row > 1:
	    if row1 <= 1 or col1 <= 1:
	        break
	    while col > 1:
	        final_operations.insert(0, operation[row][col])
	        row1 = operation[row][col][1]
	        col1 = operation[row][col][2]
	        row = row1
	        col = col1
	        if(col <= 1 or row <= 1):
	            break
	if row1 > 1 and col1 == 1:
	    final_operations.insert(0, ('D', 1, 1, row1, col1))
	elif (row1 == 1 and col1 > 1):
	    final_operations.insert(0, ('A', 1, 1, row1, col1))
	final_edits = print_actual_operations(final_operations, a, b)
	return final_edits


def print_actual_operations(arr, str1, str2):
    f_edits = ''
    for a in arr:
        if a[0] == 'S':
            if a[3] == 1:
                #print "Substitute " + str1[a[1]-1] + " with " + str2[a[2]-1] + " in " + str1 + " at position " + str(a[2])
                correction = str1[a[1]-1]
                replacement = str2[a[2]-1]
                if (len(f_edits) > 0) :
                    f_edits = f_edits + '+'
                f_edits = f_edits + str(correction + "|" + replacement)
        elif a[0] == 'D':
            #print "Delete " + str1[a[1]-1] + " from position " + str(a[1]) + " in " + str1
            tail = ''
            if a[1] - 1 > 0:
                tail = str1[a[1]-2]
            correction = tail + str1[a[1]-1]
            replacement = tail
            if (len(f_edits) > 0) :
                f_edits = f_edits + '+'
            f_edits = f_edits + str(correction + "|" + replacement)
            
        elif a[0] == 'A':
            #print "Insert " + str2[a[2]-1] + " at position " + str(a[1]) + " in " + str1
            tail = ''
            if a[1] - 1 > 0:
                tail = str1[a[1]-2]
            correction = tail + str2[a[2]-1]
            replacement = tail
            if (len(f_edits) > 0) :
                f_edits = f_edits + '+'
            f_edits = f_edits + str(correction + "|" + replacement)
                        
        else:
            #print "Transpose " + str1[a[1]-1] + " with " + str1[a[4]-1] + " which includes deleting/inserting the characters in between"
            correction = str1[a[1]-1] + str1[a[4]-1]
            replacement = str1[a[4]-1] + str1[a[1]-1]
            if (len(f_edits) > 0) :
                f_edits = f_edits + '+'
            f_edits = f_edits + str(correction + "|" + replacement)
            if(a[4] - a[1] > 1):
                temp = a[1] + 1
                while temp < a[4]:
                    #print "Delete " + str1[temp-1]
                    temp = temp + 1
                    if temp - 1 > 0:
                        tail = str1[temp-3]
                    correction = tail + str1[temp-2]
                    replacement = tail
                    if (len(f_edits) > 0) :
                        f_edits = f_edits + '+'
                    f_edits = f_edits + str(correction + "|" + replacement)
                    
            if(a[5] - a[2] - 1 > 1):
                temp = a[2] + 1
                while temp < a[5] - 1:
                    #print "Insert " + str2[temp-1]
                    temp = temp + 1

    return f_edits
    
    
def dict_words(dictfile="/usr/share/dict/american-english"):
    "Return an iterator that produces words in the given dictionary."
    return ifilter(len,
                   imap(str.strip,
                        open(dictfile)))

def timeof(fn, *args):
    import time
    t = time.time()
    res = fn(*args)
    print "time: ", (time.time() - t)
    return res

if __name__ == "__main__":
    print damerau_levenshtein_distance('abc', 'cba')

    tree = BKTree(damerau_levenshtein_distance,
                  dict_words('/usr/share/dict/american-english'))
    vocabulary = []
    iterator = dict_words('/usr/share/dict/american-english')
    for i in iterator:
        vocabulary.append(i)
    
    dist = 2
    while True:
        print "Press 0 to exit"
        i = str(raw_input("Please enter the word : "))
        if i == '0':
            break
        edit_0 = [];
        edit_1 = [];
        edit_2 = [];
        w = set(tree.query(i, dist)) - set([i]) #Candidates!
        max_val = 0;
        max_candidate = 0
        for pair in w:
            print i + " : " + pair[1]
            if pair[0] == 0:
                edit_0.append(pair[1])
            elif pair[0] == 1:
                edit_1.append(pair[1])
            else: 
                edit_2.append(pair[1])
            ed = get_edits(i, pair[1])
            if(Pedit(ed) > max_val):
                max_val = Pedit(ed)
                max_candidate = pair[1]
        print "The most likely replacement for " + i + " is : " + str(max_candidate)    
        #print edit_0
        #print edit_1
        #print edit_2
