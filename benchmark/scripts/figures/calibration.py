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
                amq = np.loadtxt(seq_amq(genome, mapper, N, L, p))
                
                # plot points with non-infinite quality
                mask = ~np.isinf(amq[:,2])
                x = amq[mask,0]
                y = amq[mask,2]
                z = amq[mask,1]
                z = z / z.sum() * 1000
                ax.scatter(x, y,
                        s=z, color=plot_colors[mapper], alpha=0.5)

                # points with infinite quality
                fake_x = amq[~mask, 0]
                fake_z = amq[~mask, 1]
                n_errors_expected = 10**(-fake_x/10) * fake_z
                claims_true = n_errors_expected < 1
                fake_y = np.zeros_like(fake_x)
                fake_y[claims_true] = fake_x[claims_true]
                fake_y[~claims_true] = -10 * np.log10(1.0/fake_z[~claims_true])
                fake_y[~claims_true][fake_y[~claims_true] > maxqual] = maxqual
                fake_z = fake_z / fake_z.sum() * 1000
                ax.scatter(fake_x[claims_true], fake_y[claims_true],
                        s=fake_z[claims_true], edgecolors=plot_colors[mapper], facecolors='none',
                           linewidths=1.2)
                ax.scatter(fake_x[~claims_true], fake_y[~claims_true], marker='s',
                        s=fake_z[~claims_true], edgecolors=plot_colors[mapper], facecolors='none',
                           linewidths=1.2)
                amq[~mask, 2] = fake_y
                ax.plot(amq[:,0], amq[:,2], '--', label=mapper)

            ax.set_title('L = %d, p = %s'%(L, p))
            m, M = ax.get_xlim()
            if M > maxqual :
                ax.set_xlim(m, maxqual+5)
            X = np.arange(m, M, 1)
            m, M = ax.get_ylim()
            if M > maxqual :
                ax.set_ylim(m, maxqual+5)
            ax.plot(X, X, 'k--', linewidth=0.75)
            if i==0 and j==0 :
                plt.legend(loc='upper left')

    fig.suptitle('%s'%(genome_aliases[genome]))
    fig.text(sup_xlabel_x, sup_xlabel_y, 'Reported Quality', ha='center')
    fig.text(sup_ylabel_x, sup_ylabel_y, 'Real Quality', va='center', rotation='vertical')
    fig.savefig('%s/data/figures/%s-calibration.pdf'%(sesame_bm_root,genome_aliases[genome]))
