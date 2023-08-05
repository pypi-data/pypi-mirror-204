#===============================================================================
# saturation.py
#===============================================================================

"""Calculate and plot saturation curves"""

# Imports ======================================================================

import os.path
import pandas as pd
import seaborn as sns
from collections import Counter
import numpy as np
from math import prod
from itertools import chain



# Constants ====================================================================

COLOR_PALETTE = sns.color_palette().as_hex()




# Functions ====================================================================

def sat_values_conf(pk_results):
    pkr = pk_results
    sc_matrix = np.zeros((pkr.number_of_genomes,pkr.number_of_genomes))
    for _, score in pkr:
        expanded_score = np.array(
            tuple(int(b) for b in f"{int.from_bytes(score, byteorder='big'):0{pkr.number_of_genomes}b}"))
        sc_matrix[sum(expanded_score) - 1,:] += expanded_score
    sc_df = pd.DataFrame(sc_matrix, index=range(1, pkr.number_of_genomes+1),
        columns=tuple(str(os.path.basename(g)).replace('.fasta.gz', '').replace('.fa.gz', '')
                      for g in pkr.genomes))
    g = len(sc_df.columns)
    coef_matrix_total = np.matrix([[prod((g-s-i)/(g-1-i) for i in range(n)) for n in range(g)]
                            for s in range(1,g+1)])
    coef_matrix_core = np.flip(coef_matrix_total.copy(), axis=0)
    for n in range(1,g):
        coef_matrix_total[:,n] += coef_matrix_total[:,n-1]
    sat_df_core = pd.DataFrame(sc_df.transpose().dot(coef_matrix_core).transpose())
    sat_df_total = pd.DataFrame(sc_df.transpose().dot(coef_matrix_total).transpose())
    sat_df = pd.concat((sat_df_total, sat_df_core))
    sat_df['n_genomes']= tuple(range(1,g+1))*2
    plotting_data = sat_df.melt(
        id_vars=['n_genomes'], value_name='n_kmers')
    del plotting_data['variable']
    plotting_data['sequence'] = (('total',) * g + ('core',) * g) * g
    return plotting_data


def sat_values(pk_results):
    """Calculate saturation curve

    Parameters
    ----------
    pk_results
        a PKResults object

    Yields
    -------
        saturation curve values
    """

    pkr = pk_results
    g = pkr.number_of_genomes
    score_dist = Counter(sum(int(b) for b in f"{int.from_bytes(score, byteorder='big'):b}")
                         for _, score in pkr)
    for n_genomes in range(1, g+1):
        yield n_genomes, sum((1-prod((g-s-n)/(g-n) for n in range(n_genomes)))*score_dist[s]
                  for s in range(1, g+1)), 'total'
        yield n_genomes, sum(prod((s-n)/(g-n) for n in range(n_genomes))*score_dist[s]
                  for s in range(1, g+1)), 'core'


def sat_plot(plotting_data, output, title: str = 'Saturation',
             linewidth: int = 3, palette=COLOR_PALETTE[:2], alpha=1, width=4,
             height=3):
    ax = sns.lineplot(x='n_genomes', y='n_kmers', hue='sequence',
                      data=plotting_data, linewidth=linewidth,
                      palette=palette, alpha=alpha)
    ax.set_title(title)
    for line in ax.legend().get_lines():
        line.set_linewidth(linewidth)
        line.set_alpha(alpha)
    fig = ax.get_figure()
    fig.set_figwidth(width)
    fig.set_figheight(height)
    fig.tight_layout()
    fig.savefig(output)
    fig.clf()


def saturation(pk_results, output=None, title: str = 'Saturation', linewidth: int = 3,
               palette=COLOR_PALETTE[:2], alpha=1, width=4, height=3,
               conf=False):
    if conf:
        sat_df = sat_values_conf(pk_results)
    else:
        sat_df = pd.DataFrame(sat_values(pk_results),
                              columns=('n_genomes', 'n_kmers', 'sequence'))
    if output:
        sat_plot(sat_df, output, title=title, linewidth=linewidth,
                 palette=palette, alpha=alpha, width=width, height=height)
    return sat_df
