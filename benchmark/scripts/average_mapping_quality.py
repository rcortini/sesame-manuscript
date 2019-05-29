import numpy as np
import sys, os

def average_mapping_quality(accuracy_fname, bin_min, bin_max, bin_step) :
    
    # generate bins
    bins = np.arange(bin_min, bin_max+bin_step, bin_step)
    
    # initialize the array
    qvals_binned = np.zeros(len(bins)-1, dtype=np.float32)
    mapq_binned = np.zeros(len(bins)-1, dtype=np.float32)
    
    with open(accuracy_fname, 'r') as fin :
        
        nunmapped = 0
        
        # parse the file line by line
        for lineno, line in enumerate(fin) :
            
            # get the values of mapping quality and truth
            mapq, is_true = line.strip('\n').split()
                          
            # get the index of the map_q_binned that we need to increment
            i = (int(mapq)-bin_min)//bin_step
            try :
                qvals_binned[i] += 1
            except IndexError :
                print(line)
                print(bins)
                print(i)
                break
            if int(is_true) == 1 :
                mapq_binned[i] += 1
                
    # once we finished parsing the file, we get the values of q, and
    # define our output array
    mapq_binned /= qvals_binned
    
    return -10 * np.log10(1-mapq_binned)

# check for proper invocation
if len(sys.argv) < 2 :
    print("Usage: average_mapping_quality <accuracy_file>", file=sys.stderr)
    sys.exit(1)

# get parameters from command line
accuracy_fname = sys.argv[1]

# launch the calculation
amq = average_mapping_quality(accuracy_fname, 0, 65, 5)

# build output file name
amq_fname = accuracy_fname.strip('.accuracy') + '.amq'

# save results to output
np.savetxt(amq_fname, amq)
