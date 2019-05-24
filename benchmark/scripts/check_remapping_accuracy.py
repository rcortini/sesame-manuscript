import sys, os
import numpy as np

def parse_smmfdp_output(samfile, out_fname, nucleotide_tolerance = 10) :
    
    with open(samfile, 'r') as fin, open(out_fname, 'w') as fout :
        
        for line in fin :
        
            if line[0] == '>' :
                seq_name = line[1:].split('\t')[0]
                # parse the seq_name
                true_chromosome, true_start, true_end  = seq_name.split(';')
            else :
                # parse the line
                try :
                    seq, temp, mapq = line.strip('\n').split()
                except ValueError :
                    print(line)
                    continue
                
                # if mapper failed, continue
                if temp == 'NA' :
                    continue
                
                # otherwise, parse the `temp`
                chromosome, start, strand = temp.split(':')
                if float(mapq) <= 0.0 :
                    continue
                else :
                    try :
                        mapq = int(-10*np.log10(float(mapq)))
                    except ValueError :
                        continue
                
                # now let's check what the mapper says

                # if mapper failed to identify chromosome...
                if true_chromosome != chromosome :
                    fout.write("%d 0\n"%(mapq))

                # let's see if it really identified the sequence...
                else :
                    if np.abs(int(true_start) - int(start)) < nucleotide_tolerance :
                        fout.write("%d 1\n"%(mapq))
                    else :
                        fout.write("%d 0\n"%(mapq))

def parse_samfile(samfile, out_fname, nucleotide_tolerance = 10) :
    with open(samfile, 'r') as fin, open(out_fname, 'w') as fout:
        nseqs = 0
        for line in fin :
            
            if line[0] == '@' :
                continue
            
            # if we're here, we're reading a sequence
            nseqs += 1
            
            # parse the line
            seq_name, flag, chromosome, start, mapq = line.split()[0:5]
            
            # if mapper failed, continue
            if chromosome == '*' :
                continue
            
            # now let's check what the mapper says
            mapq = int(mapq)
            
            # parse the seq_name
            true_chromosome, true_start, true_end  = seq_name.split(';')
            
            # if mapper failed to identify chromosome...
            if true_chromosome != chromosome :
                fout.write("%d 0\n"%(mapq))
            
            # let's see if it really identified the sequence...
            else :
                if np.abs(int(true_start) - int(start)) < nucleotide_tolerance :
                    fout.write("%d 1\n"%(mapq))
                else :
                    fout.write("%d 0\n"%(mapq))

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
out_fname = '%s.accuracy'%(samfile)

is_true_samfile = True
with open(samfile, 'r') as fin :
    line = fin.readline()
    if line[0] == '>' :
        is_true_samfile = False

if not is_true_samfile :
    parse_smmfdp_output(samfile, out_fname)
else :
    parse_samfile(samfile, out_fname)
