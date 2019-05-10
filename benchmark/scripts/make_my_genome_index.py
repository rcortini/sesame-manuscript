import sys, os

# check for proper invocation
if len(sys.argv) < 2 :
    print("Usage: make_my_genome_index.py <genome_file>", file=sys.stderr)
    sys.exit(1)

# parse command line arguments
genome_file = sys.argv[1]

# build output file
out_file = '%s.myindex'%(genome_file)

with open(genome_file, 'r') as fin, open(out_file, 'w') as fout :

    # iterate over all the lines in the file
    for line in iter(fin.readline, '') :

        # if the line starts with >, then it's a new chromosome
        if line[0] == '>' :

            # parse the line and extract the name of the chromosome
            chromosome = line.split(' ')[0][1:]

            # the current position will be the position of the newline after the
            # name of the chromosome
            pos = fin.tell()

            # print chromosome name and position
            fout.write("%s %d\n"%(chromosome, pos))
