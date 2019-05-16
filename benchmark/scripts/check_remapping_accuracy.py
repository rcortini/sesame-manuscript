import sys, os
import numpy as np

# check for proper invocation
if len(sys.argv) < 2 :
    print("Usage: check_remapping_accuracy.py <samfile>")
    sys.exit(1)

# parse command line arguments
samfile = sys.argv[1]

# check that input file exists
if not os.path.exists(samfile) :
    print("Input file %s not found"%(in_fname))
    sys.exit(1)

# init variables for analysis
mapping_quality = []
nucleotide_tolerance = 10
out_fname = '%s.accuracy'%(samfile)

with open(samfile, 'r') as fin, open(out_fname, 'w') as fout:
    nseqs = 0
    nunmapped = 0
    for line in fin :
        
        if line[0] == '@' :
            continue
        
        # if we're here, we're reading a sequence
        nseqs += 1
        
        # parse the line
        seq_name, flag, chromosome, start, mapq = line.split()[0:5]
        
        # if mapper failed, continue
        if chromosome == '*' :
            nunmapped += 1
            continue
        
        # now let's check what the mapper says
        mapq = int(mapq)
        
        # parse the seq_name
        true_chromosome, true_start, true_end  = seq_name.split(';')
        
        # if mapper failed to identify chromosome...
        if true_chromosome != chromosome :
            fout.write("* 0\n")
        
        # let's see if it really identified the sequence...
        else :
            if np.abs(int(true_start) - int(start)) < nucleotide_tolerance :
                fout.write("%d 1\n"%(mapq))
            else :
                fout.write("%d 0\n"%(mapq))
