import sys, os
import numpy as np
import time

def time_string () :
    return time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime ())

def error_message (program_name, message) :
    full_message = "%s %s: ERROR: %s"%(time_string (), program_name, message)
    print (full_message, file=sys.stderr)

def log_message (program_name, message) :
    full_message = "%s %s: INFO: %s"%(time_string (), program_name, message)
    print (full_message)

valid_DNA_chars = ('A', 'T', 'G', 'C')
mutations = {
    'A' : ['C', 'G', 'T'],
    'a' : ['C', 'G', 'T'],
    'C' : ['G', 'T', 'A'],
    'c' : ['G', 'T', 'A'],
    'G' : ['T', 'A', 'C'],
    'g' : ['T', 'A', 'C'],
    'T' : ['A', 'C', 'G'],
    't' : ['A', 'C', 'G'],
}

def parse_genome_index(index_file) :

    # prepare the iteration
    chromosomes = []
    initial_positions = []
    internal_positions = []

    # read index file line by line
    with open(index_file, 'r') as fin :
        
        for line in fin :
            
            chromosome, positions = line.strip('\n').split(':')
            positions = positions.split(',')
            
            chromosomes.append(chromosome)
            initial_positions.append(int(positions[0]))
            internal_positions.append(np.array([int(x) for x in positions], dtype=np.int64))
    
    return chromosomes, np.array(initial_positions, dtype=np.int64), internal_positions

def file_length(fin) :
    """
    Returns the length of a file handle `fin`.
    """
    fin.seek(0, os.SEEK_END)
    return fin.tell()

def extract_sequence(genome, L, chromosomes, initial_positions, internal_positions) :
    """
    Extract a single sequence of length `L` from `genome`
    """

    # get the length of the file
    flength = len(genome)
    
    # this cycle ends only when we found a valid sequence
    while True :

        # initiate the search: set number of found nucleotides "n" to zero, jump
        # to a random location in the file, set "seq" list to empty list
        n = 0
        pos = np.random.randint(low=0, high=flength-L)
        i = 0
        seq = []

        # read starting from that random location
        while n<L :

            # read a single charachter
            try :
                nucleotide = genome[pos+i]
            except IndexError :
                print(pos, i)
                break

            # if it is not a valid character, interrupt immediately the
            # iteration and go to another location. Otherwise, update seq and n.
            # In case we find a newline character, continue without updating seq
            # and n.
            if nucleotide.upper() in valid_DNA_chars :
                seq.append(nucleotide)
                n += 1
                i += 1
            elif nucleotide == '\n' :
                i += 1
                continue
            else :
                break

        # if we're here and the number of nucleotides is the number of requested
        # letters, we need to extract the position in the genome, and we're done.
        if n == L :
            
            # recall that `pos` is the position in the file where we started reading.
            # the following line of code will also work in the case in which the position
            # is in the last chromosome, because in that case the argmin function will return
            # 0, and subtracting 1 will give -1, which is the last element of the list
            # in Python.
            i = (pos >= initial_positions).argmin() - 1
            
            # we need to put in another control, which is to check that 
            if initial_positions[i+1] == pos + 1 :
                i += 1
            
            # Now we have to get the position inside the chromosome, which is the tricky
            # part. Again, we find which is the index in the "internal_positions" array,
            # which corresponds to the number of newlines from the beginning of the
            # chromosome.
            internal_position = internal_positions[i]
            j = (pos >= internal_position).argmin() - 1
            
            # now we simply need to subtract the current position from the start position,
            # and subtract the number of newlines
            start = pos - initial_positions[i] - j
            
            return chromosomes[i], start, seq

def extract_random_sequences(genome_file, N, L, mutation_rate, output_file) :

    # parse the genome index
    log_message("extract_random_sequences", "Parse genome index")
    chromosomes, initial_positions, internal_positions = \
        parse_genome_index('%s.myindex'%(genome_file))

    # open the genome file
    log_message("extract_random_sequences", "Reading genome")
    with open(genome_file, 'r') as fin :
        genome = fin.read()

    # extract the random sequences
    with open(output_file, 'w') as fout :

        # cycle on all the sequences to generate
        log_message("extract_random_sequences", "Start extracting sequences")
        for n in range(N) :

            # extract a single sequence
            chromosome, start, seq = extract_sequence(genome, L,
                                    chromosomes, initial_positions, internal_positions)
           
            # prepare the sequence for mutation
            mutated_seq = seq[:]
            
            # iterate over the nucleotides
            for j, nucleotide in enumerate(seq) :
                
                # toss a coin and see whether we mutate or not
                r = np.random.rand()
                if r > mutation_rate :
                    continue
                
                # randomly convert it into another one (not itself)
                new_nucleotide = mutations[nucleotide][np.random.randint(low=0, high=3)]
                mutated_seq[j] = new_nucleotide

            # generate the new sequence
            mutated_seq = ''.join(mutated_seq)

            # output sequence
            fout.write(">%s;%s;%s\n"%(chromosome, start, start+L))
            fout.write("%s\n"%(mutated_seq))

            # give some output, for hope
            if n%10000 == 0 :
                log_message("extract_random_sequences", "Wrote %d sequences"%(n))

if __name__ == '__main__' :

    # check for proper invocation
    if len(sys.argv) < 6 :
        print("Usage: %s <genome_file> <N> <L> <mutation_rate> <output_file>"%(sys.argv[0].split('/')[-1]))
        sys.exit(1)

    # get command line arguments
    genome_file = sys.argv[1]
    N = int(sys.argv[2])
    L = int(sys.argv[3])
    mutation_rate = float(sys.argv[4])
    output_file = sys.argv[5]

    # do the analysis
    extract_random_sequences(genome_file, N, L, mutation_rate, output_file)
