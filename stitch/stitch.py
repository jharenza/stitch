from fasta import *
from doubleblast import *
from itertools import izip, imap
from optparse import *
from multiprocessing import Pool
import os
import sys
import time
    
def main():
    parser = OptionParser(
        description="""Stitch - Tool for creating contigs from overlapping
paried-end illumina reads.""",
        usage='-i fastqfile1 -j fastqfile2')
    parser.add_option('-i', '--first', dest='filea')
    parser.add_option('-j', '--second', dest='fileb')

    (options, args) = parser.parse_args()
    
    if not (options.filea or options.fileb):
        print >> sys.stderr, 'Usage: %s %s' % \
            (parser.get_prog_name(), parser.usage)
        quit()
    
    seqsa = open(options.filea, 'r')
    seqsb = open(options.fileb, 'r')
    
    p = Pool()
     
    try:   
        for i in imap(doStitch, izip(Fasta(seqsa), \
                Fasta(seqsb))):
            if i.hits:
                pass
                #print i.contig
            else:
                # Send to duds
                pass
    except KeyboardInterrupt:
        return


def doStitch(recs):
    try:
        reca, recb = recs
        return Stitch(reca, recb)
    except KeyboardInterrupt:
        return

    
class Stitch:
    def __init__(self, reca, recb):
        self.reca = reca
        self.recb = recb
        self.hits = False
        result = Doubleblast.query(reca, recb)
        if result:
            for key in result:
                setattr(self, key, result[key])
            self._generate_contig()
            
    def _generate_contig(self): 
        if self.qstart < self.sstart:
            self.hits = True
            
            self.contig = []
            
            subject, subqual = self.recb.seq, self.recb.qual
            query, quequal = self.reca.revcomp, self.reca.qual[::-1]
            
            print self.qstart, self.qend, self.sstart, self.send
            print subject
            print query
            
            # The beginning
            self.contig.append(subject[0:self.qend-1])
            
            # The middle
            for qn, sn in zip(query, subject):
                if qn is sn:
                    self.contig.append(qn)
                else:
                    self.contig.append('X')
            
            
            # The end
            
            finalseq, finalqual = [], []
            #setattr(self, 'contig', contig)
            
            
            
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print >> sys.stderr, 'Ouch!'
        quit()