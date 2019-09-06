import numpy as np
import sys, os

def roc_curve(accuracy_fname) :

    # load accuracy file
    accuracy = np.loadtxt(accuracy_fname)
    
    # number of reads that were computed
    n = len(accuracy)
    
    # define the values of the thresholds to study
    thresholds = np.unique(accuracy[:,0])
    T = len(thresholds)
    
    # initialize
    R = np.zeros((T,2))
    
    # calculate the ROC curve
    for i, threshold in enumerate(thresholds) :
        myreads = accuracy[accuracy[:,0] >= threshold, 1]
        R[i,0] = (myreads==0).sum()/n
        R[i,1] = (myreads==1).sum()/n
    return R

# check for proper invocation
if len(sys.argv) < 2 :
    print("Usage: roc <accuracy_file>", file=sys.stderr)
    sys.exit(1)

# get parameters from command line
accuracy_fname = sys.argv[1]

# launch the calculation
R = roc_curve(accuracy_fname)

# build output file name
roc_fname = accuracy_fname.strip('.accuracy') + '.roc'

# save results to output
np.savetxt(roc_fname, R)
