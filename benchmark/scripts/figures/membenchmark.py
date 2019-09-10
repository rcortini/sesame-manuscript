from figure_settings import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import NullFormatter, LogFormatterMathtext
import sys, os

# use my custom style for the plots
plt.style.use('sesame-manuscript')

# the number of reads used for the memory benchmark
N_membenchmark = 1000000

# load memory benchmark data
maxmem = np.zeros((len(genomes), len(mappers), len(Lvals), len(pvals)), dtype=int)
exectime = np.zeros((len(genomes), len(mappers), len(Lvals), len(pvals)), dtype=int)
tps = np.zeros((len(genomes), len(mappers), len(Lvals), len(pvals)), dtype=int)
for i, genome in enumerate(genomes) :
    for j, mapper in enumerate(mappers) :
        for k, L in enumerate(Lvals) :
            for l, p in enumerate(pvals) :
                membenchmark_fname = seq_membenchmark(genome, mapper, N, L, p)
                                
                # memory and time benchmark
                mb = np.loadtxt(membenchmark_fname, dtype=int)
                maxmem[i,j,k,l] = mb[:,1].max()
                exectime[i,j,k,l] = mb[-1,0]-mb[0,0]

                # accuracy of estimate
                mba_fname = seq_mba(genome, mapper, N, L, p)
                tps[i,j,k,l] = np.loadtxt(mba_fname)/exectime[i,j,k,l]


for i, genome in enumerate(genomes) :
    fig = plt.figure(figsize=(10,8))
    gs = plt.GridSpec(2, len(Lvals), wspace=0.35, hspace=0.1)
    for k, L in enumerate(Lvals) :
        ax0 = plt.subplot(gs[0,k])
        ax1 = plt.subplot(gs[1,k])
        for j, mapper in enumerate(mappers) :
            ax0.semilogy(pvals, exectime[i,j,k,:].flatten(), 'o--', label=mapper,
                        markersize=10, alpha=0.75, color=plot_colors[mapper],
                        marker=plot_symbols[mapper])
            ax1.semilogy(pvals, tps[i,j,k,:].flatten(), 'o--',
                        markersize=10, alpha=0.75, color=plot_colors[mapper],
                        marker=plot_symbols[mapper])
            ax0.set_xticks(np.arange(0.02,0.12, 0.02))
            ax0.set_xticklabels([])
            ax1.set_xticks(np.arange(0.02,0.12, 0.02))

            # for the format of the ticks label on the y axis
            ax0.yaxis.set_major_formatter(LogFormatterMathtext())
            ax0.yaxis.set_minor_formatter(NullFormatter())
            ax1.yaxis.set_major_formatter(LogFormatterMathtext())
            ax1.yaxis.set_minor_formatter(NullFormatter())
        ax1.set_xlabel("Error rate")
        if k == 0 :
            ax0.set_ylabel("Computation time [s]")
            ax1.set_ylabel("True positives/s")
            ax0.legend()
        ax0.set_title("L = {}".format(L))
    plt.suptitle(genome_aliases[genome])
    plt.subplots_adjust(left=0.005)
    fig.savefig('%s/data/figures/%s-time_benchmark.pdf'%(sesame_bm_root,genome_aliases[genome]),
               bbox_inches='tight')

# memory usage plot
fig = plt.figure(figsize=(3,6))
l = 0
k = 0
for j, mapper in enumerate(mappers) :
    plt.semilogy(maxmem[:,j,k,l]/2**20, 'o', label=mapper, markersize=10,
                 color=plot_colors[mapper], marker=plot_symbols[mapper])
plt.xticks([0,1,2], [genome_aliases[g] for g in genomes], rotation='vertical', fontsize=18)
plt.ylabel("Maximum memory usage [Gb]")
plt.legend()
fig.tight_layout()
fig.savefig('%s/data/figures/memory_usage.pdf'%(sesame_bm_root))
