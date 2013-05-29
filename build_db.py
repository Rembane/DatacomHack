#!/usr/bin/env python2

from collections import defaultdict
import operator, sys

class Post(object):
    def __init__(self, body='', tags=None, exam=''):
        self.body = body 
        self.tags = tags 
        self.exam = exam 

    def __str__(self):
        return 'Tentamen: %s\nTaggar: %s\n\n%s' % (self.exam, ' '.join(self.tags), self.body)

class Tag(object):
    def __init__(self, body):
        while body.startswith(':'):
            body = body[1:]

        self.body  = body
        self.lower = body.lower()

    def __str__(self):
        return '%s' % self.body

    def __cmp__(self, other):
        if self.lower < other.lower:
            return -1
        elif self.lower == other.lower:
            return 0
        else:
            return 1

    def __hash__(self):
        return hash(self.lower)

posts = defaultdict(list)
cex   = ''
txt   = ''
lts   = []

with open(sys.argv[1]) as fh:
    for (i,row) in enumerate(fh): 
        # New post!
        if row.startswith('='):
            p = Post(txt, lts, cex)
            for t in lts:
                posts[t].append(p)

            txt = ''
            cex = ''
            lts = []

        # New exam!
        elif row.startswith('>'):
            cex = row.strip('> \n')

        elif row.startswith(':'):
            lts = [Tag(t) for t in row.strip().split()]

for (k,v) in sorted([(k,v) for (k,v) in posts.iteritems()], key=lambda (a,b): len(b)):
    print k, len(v)
