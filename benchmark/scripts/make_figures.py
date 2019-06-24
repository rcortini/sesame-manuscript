import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
import sys, os
# root directory of the benchmark project
sesame_bm_root = '%s/work/CRG/projects/sesame-manuscript/benchmark'%(os.getenv('HOME'))
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

def seq_root(genome, N, L, p) :
    return '%s-%d-%d-%s'%(genome, N, L, p)

def seq_fasta(genome, N, L, p, sesame_bm_root = sesame_bm_root) :
    gd = genome_dir(genome, sesame_bm_root)
    return '%s/random_sequences/%s.fasta'%(gd, seq_root(genome, N, L, p))

def seq_sam(genome, mapper, N, L, p, sesame_bm_root = sesame_bm_root) :
    seq = seq_root(genome, N, L, p)
    gd = genome_dir(genome, sesame_bm_root)
    return '%s/%s/%s.sam'%(gd, mapper, seq)

def seq_accuracy(genome, mapper, N, L, p, sesame_bm_root = sesame_bm_root) :
    return '%s.accuracy'%(seq_sam(genome, mapper, N, L, p, sesame_bm_root))

def seq_amq(genome, mapper, N, L, p, sesame_bm_root = sesame_bm_root) :
    return '%s.amq'%(seq_sam(genome, mapper, N, L, p, sesame_bm_root))

genome_aliases = {'GCA_000404065.3_Ptaeda2.0_genomic' : 'Pine',
                  'dmel-all-chromosome-r6.27' : 'Drosophila',
                  'hg38' : 'Human'}
N = 50000000

for genome in genomes :
    # init figure
    fig = plt.figure(figsize=(12, 10))
    gs = plt.GridSpec(len(Lvals), len(pvals), hspace=0.5, wspace=0.3)

    plot_colors = {'smmfdp' : 'g',
                   'bwa' : 'b',
                   'bowtie2' : 'r'} 

    for i, L in enumerate(Lvals) :
        for j, p in enumerate(pvals) :
            ax = plt.subplot(gs[i,j])
            for mapper in mappers :
                try :
                    if os.path.exists(seq_amq(genome, mapper, N, L, p)) :
                        amq = np.loadtxt(seq_amq(genome, mapper, N, L, p))
                        x = amq[~np.isinf(amq[:,1]),0]
                        y = amq[~np.isinf(amq[:,1]),1]
                        ax.plot(x, y, 'o--',
                                markersize=3, label=mapper, color=plot_colors[mapper])
                except IndexError :
                    continue

                ax.set_title('L = %d, p = %s'%(L, p), fontsize=16)
                ax.plot(x, x, 'k--', linewidth=0.75)

    plt.legend(loc='upper left')
    fig.suptitle('%s'%(genome_aliases[genome]), fontsize=32)
    fig.text(0.5, 0.07, 'Reported Quality', ha='center', fontsize = 24)
    fig.text(0.04, 0.5, 'Real Quality', va='center', rotation='vertical', fontsize = 24)
    fig.savefig('%s/data/figures/%s-benchmark.png'%(sesame_bm_root,genome_aliases[genome]))
