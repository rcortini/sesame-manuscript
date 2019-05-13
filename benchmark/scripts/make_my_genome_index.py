import sys, os

# check for proper invocation
if len(sys.argv) < 2 :
    print("Usage: make_my_genome_index.py <genome_file>", file=sys.stderr)
    sys.exit(1)

# parse command line arguments
genome_file = sys.argv[1]

# build output file
out_file = '%s.myindex'%(genome_file)

with open(genome_file, 'r') as fin, open(out_file, 'w') as fout:
    
    # init chromosome counter
    n = 0

    # iterate over all the lines in the file
    for line in iter(fin.readline, '') :

        # Get the current position in the file handle. This will be the
        # position of the newline character that terminated the current
        # line.
        pos = fin.tell()

        # if the line starts with >, then it's a new chromosome
        if line[0] == '>' :

            # parse the line and extract the name of the chromosome
            chromosome = line.split(' ')[0][1:]

            # write a newline if chromosome counter is greater than 0.
            if n>0 :
                fout.write("\n")

            # init the string associated to the new chromosome
            fout.write("%s:%d"%(chromosome, pos))

            # increment chromosome counter
            n += 1

        else :
            fout.write(",%d"%(pos))
