import pandas as pd

def count_kmers(*pk_results, names=None):
    """Count total and diagnostic K-mers in one or more indexes

    Parameters
    ----------
    pk_results
        a PKResults object
    names
        an iterable of the names for each input index

    Returns
    -------
    DataFrame
        table of total and diagnostic K-mer counts for each index
    """

    kmer_counts = pd.DataFrame(columns=('index', 'total', 'diagnostic'))
    for pkr, name in zip(pk_results, names or range(len(pk_results))):
        total_count, diagnostic_count = 0, 0
        for _, score in pkr:
            total_count += 1
            if sum(score) < pkr.number_of_genomes:
                diagnostic_count += 1
        kmer_counts = pd.concat((kmer_counts, pd.DataFrame(
            ((name, total_count, diagnostic_count),),
            columns=('index', 'total', 'diagnostic'))))
    return kmer_counts
