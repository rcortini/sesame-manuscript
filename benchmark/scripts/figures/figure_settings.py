import subprocess
import numpy as np

def getGitRoot():
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')

sesame_bm_root = '%s/benchmark'%(getGitRoot())
genomes_dir = '%s/data/genomes'%(sesame_bm_root)

# input configuration files
input_conf_dir = '%s/input_conf'%(sesame_bm_root)
genomes_fname = '%s/genomes.txt'%(input_conf_dir)
mappers_fname = '%s/mappers.txt'%(input_conf_dir)
Lvals_fname = '%s/Lvals.txt'%(input_conf_dir)
pvals_fname = '%s/pvals.txt'%(input_conf_dir)

def get_genomes(genomes_fname) :
    genomes = []
    with open(genomes_fname, 'r') as fin :
        for line in fin :
            genome = '.'.join(line.split()[0].split('/')[-1].strip('.gz').split('.')[:-1])
            genomes.append(genome)
    return genomes

def get_mappers(mappers_fname) :
    mappers = []
    with open(mappers_fname, 'r') as fin :
        for line in fin :
            mapper = line.split()[0]
            mappers.append(mapper)
    return mappers

# parse input configuration files
genomes = get_genomes(genomes_fname)
mappers = get_mappers(mappers_fname)
Lvals = np.loadtxt(Lvals_fname, dtype=int)
pvals = np.loadtxt(pvals_fname)

def genome_dir(genome, sesame_bm_root = sesame_bm_root) :
    return '%s/data/genomes/%s'%(sesame_bm_root, genome)

def mapper_dir(genome, mapper, sesame_bm_root = sesame_bm_root) :
    gd = genome_dir(genome, sesame_bm_root)
    return '%s/%s'%(gd, mapper)

def seq_root(genome, N, L, p) :
    return '%s-%d-%d-%s'%(genome, N, L, p)

def seq_fasta(genome, N, L, p, sesame_bm_root = sesame_bm_root) :
    gd = genome_dir(genome, sesame_bm_root = sesame_bm_root)
    return '%s/random_sequences/%s.fasta'%(gd, seq_root(genome, N, L, p))

def seq_sam(genome, mapper, N, L, p, sesame_bm_root = sesame_bm_root) :
    seq = seq_root(genome, N, L, p)
    md = mapper_dir(genome, mapper, sesame_bm_root = sesame_bm_root)
    return '%s/%s.sam'%(md, seq)

def seq_accuracy(genome, mapper, N, L, p, sesame_bm_root = sesame_bm_root) :
    return '%s.accuracy'%(seq_sam(genome, mapper, N, L, p, sesame_bm_root = sesame_bm_root))

def seq_amq(genome, mapper, N, L, p, sesame_bm_root = sesame_bm_root) :
    return '%s.amq'%(seq_sam(genome, mapper, N, L, p, sesame_bm_root = sesame_bm_root))

def seq_roc(genome, mapper, N, L, p, sesame_bm_root = sesame_bm_root) :
    return '%s.roc'%(seq_sam(genome, mapper, N, L, p, sesame_bm_root = sesame_bm_root))

def seq_membenchmark(genome, mapper, N, L, p, sesame_bm_root = sesame_bm_root) :
    seq = seq_root(genome, N, L, p)
    md = mapper_dir(genome, mapper, sesame_bm_root = sesame_bm_root)
    return '%s/%s.membenchmark'%(md, seq)

def seq_mba(genome, mapper, N, L, p, sesame_bm_root = sesame_bm_root) :
    seq = seq_root(genome, N, L, p)
    md = mapper_dir(genome, mapper, sesame_bm_root = sesame_bm_root)
    return '%s/%s/%s.mba'%(gd, mapper, seq)

# aliases of the genomes, so to make plots human-readable
genome_aliases = {'GCA_000404065.3_Ptaeda2.0_genomic' : 'Pine',
                  'dmel-all-chromosome-r6.27' : 'Drosophila',
                  'hg38' : 'Human'}

# colors and symbols of the mappers in the plots
plot_colors = {'smmfdp' : 'k',
               'bwa' : 'b',
               'bowtie2' : 'r'} 

plot_symbols = {'smmfdp' : 'x',
                'bwa' : '^',
                'bowtie2' : 's'} 

# constants of calculations
N = 50000000
maxqual = int(round(np.log10(N)*10))

# constants for plotting
fig_x = 12
fig_y = 10
fig_hspace = 0.3
fig_vspace = 0.3
sup_xlabel_x = 0.5
sup_xlabel_y = 0.02
sup_ylabel_x = 0.04
sup_ylabel_y = 0.5
