import sys
import numpy as np
from Bio import SeqIO
from Bio.Alphabet import IUPAC

def extract_random_sequences(chromosomes, N, L) :
    """
    This function extracts N random sequences of length L from the chromosomes.
    Takes care of excluding sequences that includes 'N'.
    """
    # get chromosome names and lengths
    chromosome_names = [k for k in chromosomes.keys()]
    chromosome_lengths = [len(l) for l in chromosomes.values()]
    chromosome_n = len(chromosomes)

    # calculate probability vector
    total_length = sum(chromosome_lengths)
    p = np.array([chromosome_lengths[i]/total_length for i in range(chromosome_n)])
    
    # iterate over the indices of the chromosome found
    n = 0
    seqs = {}
    while n<N :
        i = np.random.choice(chromosome_n, p=p)
        chromosome = chromosome_names[i]
        nmax = chromosome_lengths[i]-L
        start = np.random.randint(low=0, high=nmax)
        end = start + L
        seq = chromosomes[chromosome][start:end]
        
        # check that the sequence does not contain 'N's
        if 'N' in seq :
            continue
        n += 1
        
        seqs[(chromosome, start, end)] = seq
    
    # return the sequences we found
    return seqs

def mutate_sequences(sequences, L, mutation_rate) :
    """
    This function takes the sequence dictionary `sequences` that contains
    sequences of length `L`, and performs mutations with probability
    `mutation_rate`.
    """
    
    # init mutations
    mutations = {
        'A' : ['C', 'G', 'T'],
        'C' : ['G', 'T', 'A'],
        'G' : ['T', 'A', 'C'],
        'T' : ['A', 'C', 'G']
    }
    
    # iterate over all the sequences that we passed to the function
    mutated_sequences = {}
    for loc, sequence in sequences.items() :
        
        # prepare the sequence
        seq = list(str(sequence))
        mutated_seq = seq[:]
        
        # iterate over the nucleotides
        for n, nucleotide in enumerate(seq) :
            
            # toss a coin and see whether we mutate or not
            r = np.random.rand()
            if r > mutation_rate :
                continue
            
            # randomly convert it into another one (not itself)
            new_nucleotide = mutations[nucleotide][np.random.randint(low=0, high=3)]
            mutated_seq[n] = new_nucleotide

        # generate the new sequence
        mutated_sequences[loc] = ''.join(mutated_seq)
    
    # return
    return mutated_sequences

def output_fasta(sequences, out_fname) :
    """
    Outputs the sequences contained in the dictionary `sequences` to a fasta
    file named `out_fname`, giving as a name the location of the sequences.
    """
    with open(out_fname, 'w') as fout :
        for loc, sequence in sequences.items() :
            chromosome, start, end = loc
            fout.write(">%s;%s;%s\n"%(chromosome, start+1, end+1))
            fout.write("%s\n"%(sequence))

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
    genome = SeqIO.index(genome_file,'fasta', alphabet=IUPAC.unambiguous_dna)

    # extract the sequences of the chromosomes from the genome
    chromosomes = {}
    for key, chromosome in genome.items() :
        chromosomes[key] = str(chromosome.seq)
        
    # do the analysis
    seqs = extract_random_sequences(chromosomes, N, L)
    mutated_seqs = mutate_sequences(seqs, L, mutation_rate)
    output_fasta(mutated_seqs, output_file)
