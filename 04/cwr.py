#!/usr/bin/env python

import optparse
import sys

def load_dict (fname):
    with open(fname, "r") as f:        
        words = []
        for line in f.readlines ():
            words.extend (line.split ())
        return words

def pad (n, l, pad = None):
    k = 0
    for i in l:
        k += 1
        yield i
    while k < n:
        k += 1
        yield pad
    
class Vertex:    
    def __init__ (self, word, parent = None):
        self.parent = parent
        self.word = word
        self.depth = (parent and parent.depth + 1) or 0

    def words (self):
        if self.parent:
            for word in self.parent.words ():
                yield word
        yield self.word

    def __str__ (self):
        (a, b, c, d) = pad (4, self.words (), "...")
        return """\
%s
%s#%s
%s%s%s""" % (a, b[1], c[1], b[2], d[1], c[2])

    def valid (self):
        (a, b, c, d) = pad (4, self.words ())
        class CheckFailed (Exception):
            pass
        
        def check (b):
            if not b:
                raise CheckFailed ()

        try:
            check (a[0] == b[0])
            check (a[2] == c[0])
            check (b[2] == d[0])
            check (c[2] == d[2])
        except CheckFailed:
            return False
        except TypeError:
            pass
        return True
                   

    def children (self, dict):
        for w in dict:
            child = Vertex (w, self)
            if child.valid ():
                yield child

parser = optparse.OptionParser(description='3x3 crossword puzzle solver',
                               usage = "Usage: %prog [options] word")
parser.add_option ("--words", metavar = "filename", type = "string", dest = "dict", default = "words.txt",
                   help = 'Word list (defaults to %default)')

(options, args) = parser.parse_args ()
if len (args) != 1:
    parser.print_help ()
    sys.exit (0)
    
dict = load_dict (options.dict)
initial_word = args[0].upper ()

def solve_dfs (initial):
    def search_dfs (v):
        global dict
        if v.depth == 3:
            yield v
        else:            
            for child in v.children (dict):                
                for sol in search_dfs (child):
                    yield sol
                    
    return search_dfs (Vertex (initial))

for sol in solve_dfs (initial_word):
    print sol
    print

