#!/usr/bin/env python

import pysam 
import sys
bamfile = pysam.AlignmentFile(sys.argv[1],'rb')
print bamfile
r1 = bamfile.fetch("chr15", 28364418, 28364419)
rn1 = set([read.query_name for read in r1])
r2 = bamfile.fetch("chr15", 28364427, 28364428)
rn2 = set([read.query_name for read in r2])
print "reads overlapping SNP1: ",len(rn1) 
print "reads overlapping SNP2: ",len(rn2)
print "reads fit for phasing: ",len(rn1.intersection(rn2))
