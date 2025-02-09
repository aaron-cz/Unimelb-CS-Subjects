#!usr/lib/python2.7
# Auther    : Haonan Li <haonanl5@student.unimelb.edu.au>
# Porpuse   : Naive alignment for a FASTQ read file

import os
import sys
import getopt

# Reverse a read
def reverse(read):
    reverse_read = ""
    read = read[::-1]   #reverse the read
    # get comlimentary read
    for i in range(len(read)):
        if read[i] == 'A':
            reverse_read += 'T'
        elif read[i] == 'T':
            reverse_read += 'A'
        elif read[i] == 'G':
            reverse_read += 'C'
        elif read[i] == 'C':
            reverse_read += 'G'
    return reverse_read


# Compute hamming distance less than 3
def hamming_dis(a,b):
    dis = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            dis += 1
        # treat read with distance larger than 2 not aligned
        if dis > 2:
            return dis
    return dis

# Read two files
def init(ref_file, read_file):
    
    # Reference
    ref_f = open(ref_file, "r")
    line = ref_f.readline()
    line = line.strip()
    ref_name = line[1:]
    ref = ">"
    for line in ref_f.readlines():
        line = line.strip()
        ref += line
    ref = ref.upper()

    # Read file
    read_f = open(read_file, "r")
    reads = []
    line = read_f.readline()
    while line:
        read_name = line.strip()[1:]
        read = read_f.readline().strip()
        read_f.readline()
        read_quality = read_f.readline().strip()
        reads.append((read_name, read, read_quality))
        line = read_f.readline()
    return (ref_name, ref, reads)


# Aligner 
def alignment(ref_file, read_file, out_file):
    ref_name, ref, reads = init(ref_file, read_file)
    out_f = open(out_file, "w")
    out_f.write("READ_NEME\tREF_NAME\tPOS\tSTRAND\tNUMBER_OF_ALIGNMENTS\tHAMMING_DISTANCE\n")
    
    # read is tuple of (read_name, read_sequence, quality)
    # all reads
    for read in reads:
        min_dis = 2
        min_set = set()
        # forward search
        # all positions
        for start in range(len(ref)-len(read[1])):
            end = start + len(read[1])
            dis = hamming_dis(read[1], ref[start:end])
            if dis < min_dis:
                min_dis = dis
                min_set.clear()
                min_set.add(start)
            elif dis == min_dis:
                min_set.add(start)
        # reverse search
        if reverse(read[1]) != read[1]:
            r_read = reverse(read[1])
            # all positions
            for start in range(len(ref)-len(read[1])):
                end = start + len(read[1])
                dis = hamming_dis(r_read, ref[start:end])
                if dis < min_dis:
                    min_dis = dis
                    min_set.clear()
                    min_set.add(0-start)
                elif dis == min_dis:
                    min_set.add(0-start)
        # output 
        strand = '-'
        min_pos = 9999
        if len(min_set) == 0:
            out_f.write(read[0] + "\t*\t0\t*\t0\t*\n")
        else:
            for pos in min_set:
                if abs(pos)<min_pos:
                    min_pos = abs(pos)
                    if pos > 0:
                        strand = '+'
                    elif pos < 0:
                        strand = '-'
            out_f.write( read[0] + '\t' + ref_name + '\t' + str(min_pos) \
                            + '\t' + strand + '\t' + str(len(min_set))   \
                            + '\t' + str(min_dis) + '\n' )
        
        

# Usage of the tool
def usage():
   print ("usage:python naive_aligner.py [options] ... [-f reffile | -r readfile | ... ]")
   print ("Options and arguments:")
   print ("-h     :Help")
   print ("-f     :Reference file.")
   print ("-r     :FASTQ read file.")
   print ("-o     :Output of alignment result file.")


def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "hf:r:o:", \
        ["help", "reference=", "read=", "output="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help='):
            usage()
            sys.exit()
        elif opt in ('-f', '--reference='):
            ref_file = arg
        elif opt in ('-r', '--read='):
            read_file = arg
        elif opt in ('-o', '--output='):
            out_file = arg
    # If two essential variables has been defined
    if not('ref_file' in locals().keys()) or \
        not('read_file' in locals().keys()) or \
        not('out_file' in locals().keys()):
        usage()
        sys.exit()
       
    # main process
    alignment(ref_file, read_file, out_file)

if __name__ == "__main__":
    main(sys.argv)
