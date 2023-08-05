import pytest
import pandas as pd
import tarfile
from itertools import product, islice
from multiprocessing import cpu_count
from pankmer.download import download_example
from pankmer.index import get_kmers
from pankmer.pankmer import PKResults, run_index, retreive_metadata
from pankmer.count import count_kmers 
from pankmer.saturation import saturation
from pankmer.upset import count_scores
from pankmer.adjacency_matrix import get_adjacency_matrix
from pankmer.reg_coverage import reg_coverage, genome_coverage


@pytest.fixture(scope='session')
def example_data(tmp_path_factory):
    d = tmp_path_factory.mktemp('pk_example')
    download_example(d)
    return d / 'PanKmer_example_Sp_Chr19'


@pytest.fixture(scope='session')
def example_index(example_data):
    run_index(example_data / 'Sp_Chr19_genomes', example_data / 'Sp_Chr19_index',
        threads=cpu_count())
    return example_data / 'Sp_Chr19_index'

@pytest.fixture
def kmer_counts():
    return pd.DataFrame((('Sp_Chr19_index',  4764864, 836962),),
                        columns=('index', 'total', 'diagnostic'))

@pytest.fixture
def saturation_stats():
    return pd.DataFrame([[1, 3781561.666666667, 'total'],
                         [1, 3781561.6666666665, 'core'],
                         [2, 4415588.0, 'total'],
                         [2, 3147535.3333333335, 'core'],
                         [3, 4764864.0, 'total'],
                         [3, 2862785.0, 'core']],
                         columns=('n_genomes', 'n_kmers', 'sequence'))

@pytest.fixture
def saturation_stats_conf():
    return pd.DataFrame([[1, 3739816.0, 'total'],
                         [2, 4283764.5, 'total'],
                         [3, 4494630.5, 'total'],
                         [1, 3739816.0, 'core'],
                         [2, 3195867.5, 'core'],
                         [3, 2862785.0, 'core'],
                         [1, 3793342.0, 'total'],
                         [2, 4535271.0, 'total'],
                         [3, 5088572.0, 'total'],
                         [1, 3793342.0, 'core'],
                         [2, 3051413.0, 'core'],
                         [3, 2862785.0, 'core'],
                         [1, 3811527.0, 'total'],
                         [2, 4427728.5, 'total'],
                         [3, 4711389.5, 'total'],
                         [1, 3811527.0, 'core'],
                         [2, 3195325.5, 'core'],
                         [3, 2862785.0, 'core']],
                         columns=('n_genomes', 'n_kmers', 'sequence'))

@pytest.fixture
def upset_stats():
    return pd.Series([476995, 2862785, 283661, 188086, 189170, 553301, 210866],
        index=pd.MultiIndex.from_tuples([
            (True, False, True), (True, True, True), (False, False, True),
            (False, True, True), (True, True, False), (False, True, False),
            (True, False, False)]))

@pytest.fixture
def regcov_top_rows():
    return pd.DataFrame([['Chr19', 384628, 384629, 1.0],
                         ['Chr19', 384629, 384630, 1.0],
                         ['Chr19', 384630, 384631, 1.0],
                         ['Chr19', 384631, 384632, 1.0]])

@pytest.fixture
def genomecov_rounded():
    return pd.DataFrame([['Chr19', 0.000000, 0.979049, 0, 0],
                         ['Chr19', 0.252561, 0.932748, 0, 0],
                         ['Chr19', 0.505123, 0.971341, 0, 0],
                         ['Chr19', 0.757684, 0.964393, 0, 0],
                         ['Chr19', 1.000000, 0.979875, 0, 0]],
                         columns=('SeqID', 'Chromosome', 'K-mer coverage (%)',
                                  'Group', 'Group_chrom'))

@pytest.fixture
def test_kmers():
    return {2412807660169719871: 1, 3476510368925482027: 1, 2234894531119824834: 1}


@pytest.fixture
def metadata(example_data):
    return {"kmer_size": 31,
            "genomes": {"0": str(example_data / "Sp_Chr19_genomes" / "Sp9509_oxford_v3_Chr19.fasta.gz"),
                        "1": str(example_data / "Sp_Chr19_genomes" / "Sp7498_HiC_Chr19.fasta.gz"),
                        "2": str(example_data / "Sp_Chr19_genomes" / "Sp9512_a02_genome_Chr19.fasta.gz")},
            "genome_sizes": {str(example_data / "Sp_Chr19_genomes" / "Sp9509_oxford_v3_Chr19.fasta.gz"): 3959434,
                             str(example_data / "Sp_Chr19_genomes" / "Sp7498_HiC_Chr19.fasta.gz"): 3993341,
                             str(example_data / "Sp_Chr19_genomes" / "Sp9512_a02_genome_Chr19.fasta.gz"): 3855210},
            "positions": {"4611686018427387903": 4764863}}


@pytest.mark.slow
def test_index_from_tar_file(example_data):
    with tarfile.open(example_data / 'Sp_Chr19_genomes.tar', 'w') as tar:
        tar.add(example_data / 'Sp_Chr19_genomes')
    run_index(example_data / 'Sp_Chr19_genomes.tar', example_data / 'Sp_Chr19_index.tar',
        threads=cpu_count())

@pytest.mark.slow
def test_count(example_index, kmer_counts):
    results = PKResults(example_index)
    test_kmer_counts = count_kmers(results, names=('Sp_Chr19_index',))
    for column in 'index', 'total', 'diagnostic':
        assert test_kmer_counts.loc[0, column] == kmer_counts.loc[0, column]

@pytest.mark.slow
def test_count_from_tar_file(example_data, example_index, kmer_counts):
    with tarfile.open(example_data / 'Sp_Chr19_index.tar', 'w') as tar:
        tar.add(example_index)
    results = PKResults(example_data / 'Sp_Chr19_index.tar')
    test_kmer_counts = count_kmers(results, names=('Sp_Chr19_index',))
    for column in 'index', 'total', 'diagnostic':
        assert test_kmer_counts.loc[0, column] == kmer_counts.loc[0, column]

@pytest.mark.slow
def test_saturation(example_index, saturation_stats):
    results = PKResults(example_index)
    test_sat = saturation(results)
    for column in 'sequence', 'n_genomes', 'n_kmers':
        for i in range(6):
            assert test_sat.loc[i, column] == saturation_stats.loc[i, column]

@pytest.mark.slow
def test_upset(example_index, upset_stats):
    results = PKResults(example_index)
    test_upset = count_scores(results, results.genomes)
    for i in upset_stats.index:
        assert test_upset.loc[i] == upset_stats.loc[i]

@pytest.mark.slow
def test_saturation_conf(example_index, saturation_stats_conf):
    results = PKResults(example_index)
    test_sat = saturation(results, conf=True)
    for column in 'sequence', 'n_genomes', 'n_kmers':
        for i in range(18):
            assert test_sat.loc[i, column] == saturation_stats_conf.loc[i, column]

@pytest.mark.slow
def test_sat_from_tar_file(example_data, example_index, saturation_stats):
    with tarfile.open(example_data / 'Sp_Chr19_index.tar', 'w') as tar:
        tar.add(example_index)
    results = PKResults(example_data / 'Sp_Chr19_index.tar')
    test_kmer_counts = saturation(results)
    for column in 'sequence', 'n_genomes', 'n_kmers':
        for i in range(6):
            assert test_kmer_counts.loc[i, column] == saturation_stats.loc[i, column]

@pytest.mark.slow
def test_adjacency_matrix(example_index, adj_matrix):
    results = PKResults(example_index)
    test_adj_matrix = get_adjacency_matrix(results)
    for i, j in product(range(3), repeat=2):
        assert test_adj_matrix.iloc[i,j] == adj_matrix.iloc[i,j]


@pytest.mark.slow
def test_reg_coverage(example_data, example_index, regcov_top_rows):
    results = PKResults(example_index)
    regcov = pd.DataFrame(reg_coverage(results,
        ref=example_data / 'Sp_Chr19_genomes' / 'Sp9509_oxford_v3_Chr19.fasta.gz',
        coords='Chr19:384629-385934'))
    for i, j in product(range(4), repeat=2):
        assert regcov.iloc[i,j] == regcov_top_rows.iloc[i,j]


@pytest.mark.slow
def test_reg_coverage_gene_name(example_data, example_index, regcov_top_rows):
    results = PKResults(example_index)
    regcov = pd.DataFrame(reg_coverage(results,
        ref=example_data / 'Sp_Chr19_genomes' / 'Sp9509_oxford_v3_Chr19.fasta.gz',
        coords='Sp19g00080',
        genes=example_data / 'Sp_Chr19_features' / 'Sp9509_oxford_v3_Chr19.gff3.gz'))
    for i, j in product(range(4), repeat=2):
        assert regcov.iloc[i,j] == regcov_top_rows.iloc[i,j]


@pytest.mark.slow
def test_reg_coverage_to_file(example_data, example_index, regcov_top_rows):
    results = PKResults(example_index)
    reg_coverage(results,
        ref=example_data / 'Sp_Chr19_genomes' / 'Sp9509_oxford_v3_Chr19.fasta.gz',
        coords='Chr19:384629-385934',
        output_file=example_data / 'regcov.bdg')
    regcov = pd.read_table(example_data / 'regcov.bdg', header=None).head(4)
    for i, j in product(range(4), repeat=2):
        assert regcov.iloc[i,j] == regcov_top_rows.iloc[i,j]


@pytest.mark.slow
def test_get_kmers(example_index, upper, lower, test_kmers):
    results = PKResults(example_index)
    genomes = results.genomes
    kmers = get_kmers(upper, lower, genomes)
    assert test_kmers == dict(islice(kmers.items(), 3))

@pytest.mark.vslow
def test_retrieve_metadata(example_data, metadata):
    run_index(example_data / 'Sp_Chr19_genomes', example_data / 'Sp_Chr19_index_singlethread',
        threads=1)
    kmer_size, genomes, positions = retreive_metadata(example_data / 'Sp_Chr19_index_singlethread' / 'metadata.json')
    test_genomes = {}
    for pos in range(len(metadata['genomes'])):
        genome = metadata['genomes'][str(pos)]
        size = metadata['genome_sizes'][genome]
        test_genomes[genome] = size
    assert kmer_size == metadata['kmer_size']
    assert genomes == test_genomes 
    assert positions == metadata['positions']

@pytest.mark.vslow
def test_genome_coverage(example_data, example_index, genomecov_rounded):
    results = PKResults(example_index)
    genome_coverage(results,
        ref=str(example_data / 'Sp_Chr19_genomes' / 'Sp9509_oxford_v3_Chr19.fasta.gz'),
        chromosomes=['Chr19'],
        output=example_data / 'genomecov.svg',
        output_table=example_data / 'genomecov.tsv')
    genomecov = pd.read_table(example_data / 'genomecov.tsv')
    for i in range(4):
        assert genomecov.loc[i, 'SeqID'] == genomecov_rounded.loc[i, 'SeqID']
    for i, j in product(range(5), range(1, 5)):
        assert round(genomecov.iloc[i, j], 6) == genomecov_rounded.iloc[i, j]
