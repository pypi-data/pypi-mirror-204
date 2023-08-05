import pytest
import pandas as pd
from itertools import product
from pankmer.tree import (adj_to_jaccard,
                          adj_to_overlap,
                          compute_linkage_matrix,
                          linkage_df,
                          linkage_to_newick)


@pytest.fixture
def jaccard_matrix(genome_names):
    genomes = 'Sp9509_oxford_v3_Chr19', 'Sp7498_HiC_Chr19', 'Sp9512_a02_genome_Chr19'
    return pd.DataFrame([[1.0,3050871/4553998,3339780/4211563],
                         [3050871/4553998,1.0,3051955/4481203],
                         [3339780/4211563,3051955/4481203,1.0]],
                         index=genome_names, columns=genome_names)


@pytest.fixture
def overlap_matrix(genome_names):
    genomes = 'Sp9509_oxford_v3_Chr19', 'Sp7498_HiC_Chr19', 'Sp9512_a02_genome_Chr19'
    return pd.DataFrame([[1.0,3050871/3793342,3339780/3739816],
                         [3050871/3793342,1.0,3051955/3739816],
                         [3339780/3739816,3051955/3739816,1.0]],
                         index=genome_names, columns=genome_names)

@pytest.fixture
def jaccard_newick():
    return '(Sp7498_HiC_Chr19:0.33006755822027156,(Sp9512_a02_genome_Chr19:0.20699749712873816,Sp9509_oxford_v3_Chr19:0.20699749712873816)3:0.1230700610915334);'

@pytest.fixture
def overlap_newick():
    return '(Sp7498_HiC_Chr19:0.19573004490499402,(Sp9512_a02_genome_Chr19:0.10696675986198256,Sp9509_oxford_v3_Chr19:0.10696675986198256)3:0.08876328504301145);'


def test_adj_to_jaccard(adj_matrix, jaccard_matrix):
    test_jaccard_matrix = adj_to_jaccard(adj_matrix)
    for i, j in product(range(3), repeat=2):
        assert test_jaccard_matrix.iloc[i,j] == jaccard_matrix.iloc[i,j]


def test_adj_to_overlap(adj_matrix, overlap_matrix):
    test_overlap_matrix = adj_to_overlap(adj_matrix)
    for i, j in product(range(3), repeat=2):
        assert test_overlap_matrix.iloc[i,j] == overlap_matrix.iloc[i,j]


def test_newick(genome_names, jaccard_matrix, overlap_matrix, jaccard_newick, overlap_newick):
    assert linkage_to_newick(linkage_df(compute_linkage_matrix(jaccard_matrix)), genome_names) == jaccard_newick
    assert linkage_to_newick(linkage_df(compute_linkage_matrix(overlap_matrix)), genome_names) == overlap_newick
