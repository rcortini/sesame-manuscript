from figure_settings import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import NullFormatter, LogFormatterMathtext
import sys, os

# use my custom style for the plots
plt.style.use('sesame-manuscript')

for genome in genomes :
    # init figure
    fig = plt.figure(figsize=(fig_x, fig_y))
    gs = plt.GridSpec(len(Lvals), len(pvals), hspace=fig_hspace,
                      wspace=fig_vspace)

    # plot all cases
    for i, L in enumerate(Lvals) :
        for j, p in enumerate(pvals) :
            ax = plt.subplot(gs[i,j])
            for mapper in mappers :
                # load data
                roc = np.loadtxt(seq_roc(genome, mapper, N, L, p))

                ax.loglog(roc[:,0]+roc[:,1], roc[:,0]/(roc[:,0]+roc[:,1]), 'o',
                          label=mapper, alpha=0.5,
                          color=plot_colors[mapper], marker=plot_symbols[mapper],
                          markersize=6)
                
            m, M = ax.get_xlim()
            if M < 10**7 :
                ax.set_xlim(m, 1.2*10**7)
            ax.xaxis.set_major_formatter(LogFormatterMathtext())
            ax.xaxis.set_minor_formatter(NullFormatter())
            ax.yaxis.set_major_formatter(LogFormatterMathtext())
            ax.yaxis.set_minor_formatter(NullFormatter())
            ax.set_title('L = %d, p = %s'%(L, p))

    fig.suptitle('%s'%(genome_aliases[genome]))
    fig.text(sup_xlabel_x, sup_xlabel_y, 'Size', ha='center')
    fig.text(sup_ylabel_x, sup_ylabel_y, 'False discovery rate', va='center', rotation='vertical')
    fig.savefig('%s/data/figures/%s-roc2.pdf'%(sesame_bm_root,genome_aliases[genome]))
