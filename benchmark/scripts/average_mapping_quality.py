import numpy as np
import sys, os

def average_mapping_quality(accuracy_fname) :

    # load the file
    x = np.loadtxt(accuracy_fname)

    # initialize the arrays
    qvals = np.unique(x[:,0])
    mapq = np.zeros(len(qvals))
    qvals_counts = np.zeros(len(qvals))

    # parse the file line by line
    for q, is_true in x :

        # get the index of the map_q_binned that we need to increment
        i = np.where(qvals == q)[0][0]
        qvals_counts[i] += 1
        if int(is_true) == 1 :
            mapq[i] += 1

    # once we finished parsing the file, we get the values of q, and
    # define our output array
    mapq /= qvals_counts

    # calculate the average mapping quality
    amq = -10 * np.log10(1-mapq)

    return np.column_stack((qvals, amq))

# check for proper invocation
if len(sys.argv) < 2 :
    print("Usage: average_mapping_quality <accuracy_file>", file=sys.stderr)
    sys.exit(1)

# get parameters from command line
accuracy_fname = sys.argv[1]

# launch the calculation
amq = average_mapping_quality(accuracy_fname)

# build output file name
amq_fname = accuracy_fname.strip('.accuracy') + '.amq'

# save results to output
np.savetxt(amq_fname, amq)
