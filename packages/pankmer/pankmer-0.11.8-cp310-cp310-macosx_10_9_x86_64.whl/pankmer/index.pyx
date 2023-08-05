import time
cimport cython
from Bio import SeqIO
import gzip
import datetime
from os.path import join, getsize, exists, isfile, isdir, dirname, basename
from os import mkdir, listdir
import os
import sys
import io
from os.path import join
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.unordered_map cimport unordered_map
from libc.string cimport strcpy, strlen
from libc.stdio cimport printf
import numpy
cimport numpy
from cpython cimport array
import array
import tarfile
import math
from multiprocessing import Pool
import shutil
import json
import pandas as pd
from pankmer.gzip_agnostic_open import gzip_agnostic_open
from pankmer.version import __version__
from pankmer.populate import populate

def print_err(message):
    print(f"{datetime.datetime.now()}: {message}")


def genome_name(genome):
    return genome.split('/')[-1].split('.')[0]


boundscheck=False
wraparound=False
cpdef vector[unsigned long long] break_seq(char * seq, 
    unsigned long long upper, unsigned long long lower) nogil:
    cdef unordered_map[char, unsigned long long] btod, comp
    cdef int i, seq_size, x, N_count, k
    cdef char base
    cdef unsigned long long digiqry, digirev, digimax, kmers_template, kbit, rev_i, num, revnum
    cdef vector[unsigned long long] digimax_vec
    kmers_template = 3
    k = 31
    btod[b'A'] = 3
    btod[b'C'] = 2
    btod[b'G'] = 1
    btod[b'T'] = 0
    comp[b'A'] = 0
    comp[b'C'] = 1
    comp[b'G'] = 2
    comp[b'T'] = 3
    digiqry = 0
    digirev = 0
    N_count = 0
    seq_size = strlen(seq)
    for i in range(k-2):
        kmers_template = kmers_template<<2 | 3
    for i in range(k):
        base = seq[i]
        N_count -= 1
        if btod.find(base) == btod.end():
            N_count = k
            base = b'A'
        num = btod[base]
        revnum = comp[base]
        rev_i = revnum<<((k-1)*2)
        digiqry = ((digiqry & kmers_template)<<2) | num
        digirev = ((digirev>>2) & kmers_template) | rev_i

    if N_count <= 0:
        if digiqry >= digirev:
            digimax = digiqry
        else:
            digimax = digirev
        if ((digimax >= lower) and (digimax < upper)):
            digimax_vec.push_back(digimax)

    for i in range(k, seq_size):
        base = seq[i]
        N_count -= 1
        if btod.find(base) == btod.end():
            N_count = k
            base = b'A'
        num = btod[base]
        revnum = comp[base]
        rev_i = revnum<<((k-1)*2)
        digiqry = (((digiqry & kmers_template)<<2)) | num
        digirev = (((digirev>>2) & kmers_template)) | rev_i

        if N_count <= 0:
            if digiqry >= digirev:
                digimax = digiqry
            else:
                digimax = digirev
            if (digimax >= lower) and (digimax < upper):
                digimax_vec.push_back(digimax)

    return digimax_vec

def get_kmers(upper, lower, genomes, tar_file=''):
    # cdef unsigned long default
    # cdef unsigned long template
    cdef int gnum = len(genomes)
    # seqs = []
    k = 31
    kmers = {}
    scores = {}
    for count in range(len(genomes)):
        scores[count] = 1<<count
    if tar_file:
        tar = tarfile.open(tar_file)
    for count, genome_file in enumerate(genomes):
        print_err(f"Scoring {genome_file} ({count+1}/{gnum}).")
        if tar_file:
            infile = gzip_agnostic_open(genome_file, 'rt', tar=tar)
        else:
            infile = gzip_agnostic_open(genome_file, 'rt')
        for c, record in enumerate(SeqIO.parse(infile, 'fasta')):
            seq = bytes(str(record.seq).upper(), 'ascii')
            digimax_vec = break_seq(seq, upper, lower)
            for digimax in digimax_vec:
                if digimax in kmers:
                    kmers[digimax] = kmers[digimax] | scores[count]
                else:
                    kmers[digimax] = scores[count]
        infile.close()
        print_err(f"Finished scoring {genome_name(genome_file)}.")
    if tar_file:
        tar.close()
    return kmers


ctypedef numpy.int_t DTYPE_t
@cython.boundscheck(False)
@cython.wraparound(False) 
def add_score_mat_np(numpy.ndarray[DTYPE_t, ndim=1] score_multi, numpy.ndarray[DTYPE_t, ndim=2] mat):
    # cdef list tmp_list = []
    cdef int size = len(score_multi)
    for count in range(size):
        if score_multi[count]:
            mat[count] = numpy.add(mat[count], score_multi)
    return mat

cpdef vector[int] score_byte_to_blist(bytes b, int sz):
    cdef vector[int] vec
    cdef int k, s
    k = 0
    s = len(b)
    while k < sz:
        vec.push_back(b[s - (k//8) - 1] & (1<<(k%8)) > 0)
        k = k+1
    
    return vec


# cpdef vector[int] kmer_byte_to_blist(bytes b, int sz):
#     cdef vector[int] vec
#     cdef int k, s
#     k = sz-1
#     s = len(b)
#     while k >= 0:
#         vec.push_back(b[s - (k//8) - 1] & (1<<(k%8)) > 0)
#         k = k-1
    
#     return vec


# cpdef unsigned long long kmer_byte_to_long(bytes b, int sz):
#     cdef unsigned long long k_int, bit
#     cdef int k, s
#     k = sz*2-1
#     s = len(b)
#     k_int = 0
#     while k >= 0:
#         bit = b[s - (k//8) - 1] & (1<<(k%8)) > 0
#         k_int = k_int | (bit<<k)
#         k = k-1
    
#     return k_int

def create_index(upper, lower, kmer_bitsize, score_bitsize, genomes, outdir, tar_file=''):
    kmers = get_kmers(upper, lower, genomes, tar_file)
    sorted_kmers = sorted(kmers.keys())
    print_err(f"Saving {lower}-{upper} kmers.")
    kmers_out_path = join(outdir, f'kmers_{lower}_{upper}.b.gz')
    scores_out_path = join(outdir, f'scores_{lower}_{upper}.b.gz')
    count = 0
    kmers_post = {}
    kmer = None
    with gzip.open(kmers_out_path, 'wb') as kmers_out, gzip.open(scores_out_path,'wb') as scores_out:
        with io.BufferedWriter(scores_out, buffer_size=1000*score_bitsize) as so_buffer ,\
            io.BufferedWriter(kmers_out, buffer_size=1000*kmer_bitsize) as ko_buffer:
            for kmer in sorted_kmers:
                if count%10000000 == 0 and count != 0:
                    kmers_post[kmer] = count
                    count = 0
                score = kmers[kmer]
                ko_buffer.write(
                    kmer.to_bytes(kmer_bitsize,
                    byteorder="big", signed=False))
                so_buffer.write(
                    score.to_bytes(score_bitsize,
                    byteorder="big", signed=False))
                count += 1
            if kmer != None and kmer not in kmers_post:
                kmers_post[kmer] = count-1
    return kmers_post

def run_core_cohort(args):
    limits, genomes, outdir, index, tar_file = args
    k = 31
    gnum = len(genomes)
    kmer_bitsize = math.ceil(((k*2))/8)
    score_bitsize = math.ceil(gnum/8)
    lower, upper = limits
    # if index != None:
    #     kmers_post = update_index(upper, lower, kmer_bitsize, score_bitsize, genomes, outdir, index)
    # else:
    #     kmers_post = create_index(upper, lower, kmer_bitsize, score_bitsize, genomes, outdir, tar_file=tar_file)
    kmers_post = create_index(upper, lower, kmer_bitsize, score_bitsize, genomes, outdir, tar_file=tar_file)
    return {f'{lower}_{upper}': kmers_post}


def index_genomes(mem_split, genomes, outdir, threads, index, tar_file=''):
    k = 31
    # Get borders
    b = generate_split(mem_split, threads)
    # divide borders based on memory
    if len(b) == 0:
        mem_blocks = [[0], [(1<<63)-1]]
    else:
        divisions = math.ceil(len(b)/mem_split)
        mem_blocks = [[0]]+[b[i:i+divisions] for i in range(0, len(b), divisions)]
        mem_blocks[-1].append((1<<63)-1)
    post_dict = {}
    all_core_blocks = []
    # for each memory block
    for m in range(1, len(mem_blocks)):
        temp_core_block = [mem_blocks[m-1][-1]]
        core_blocks = []
        for border in mem_blocks[m]:
            temp_core_block.append(border)
            core_blocks.append(temp_core_block)
            all_core_blocks.append(temp_core_block)
            temp_core_block = [border]
        # Run cpu blocks concurently
        core_block_args = [[limits, genomes, outdir, index, tar_file] for limits in core_blocks]
        if threads > 1:
            core_worker = Pool(threads)
            results = core_worker.map(run_core_cohort, core_block_args)
        else:
            results = map(run_core_cohort, core_block_args)
        for result in results:
            post_dict.update(result)
                
    return post_dict, all_core_blocks


def generate_split(memory, cpu):
    x_p = []
    number_of_bits = 20
    split_num = cpu*memory
    for num in populate(1, number_of_bits):
        mask =sum([1<<i for i in range(number_of_bits+1)])
        comp = num^mask|(1<<number_of_bits)
        binned = bin(comp)[3:]
        rev = 1
        for i in range(1,number_of_bits,2)[::-1]:
            rev = (rev << 2) | int(binned[i-1:i+1],2)
        x_p.append(max(num, rev))

    p_df = pd.DataFrame([i>>6 for i in x_p])
    counts_df = p_df.value_counts().sort_index()
    counts = counts_df.values
    counts_index = counts_df.index
    mean_count = counts_df.mean()
    chunk_size = math.ceil(sum(counts)/(split_num))
    split_points = []
    s = 0
    for i in range(len(counts)):
        if s >= chunk_size-((i%2)*mean_count):
            split_points.append(counts_index[i][0])
            s = 0
        s += counts[i]
    # 64 bits split points
    sf_split_points = [i<<((31-7)*2-1) | ((1<<((31-7)*2-1))-1) for i in split_points]
    if sf_split_points:
        sf_split_points[-1] = (1<<62)
    else:
        sf_split_points = [(1<<62)]
    return sf_split_points


def concat_files(post_dict, all_core_blocks, outdir):
    positions_dict = {}
    num = 0
    with open(join(outdir, 'kmers.b.gz'), 'wb') as kmers, open(
        join(outdir, 'scores.b.gz'), 'wb') as scores:
        for lower, upper in all_core_blocks:
            temp_dict = post_dict[f"{lower}_{upper}"]
            for key in temp_dict:
                cur = temp_dict[key]
                num = cur + num
                positions_dict[key] = num
            num += 1
            with open(
                join(outdir, f'kmers_{lower}_{upper}.b.gz'), 'rb') as k, open(
                    join(outdir, f'scores_{lower}_{upper}.b.gz'), 'rb') as s:
                shutil.copyfileobj(k, kmers)
                shutil.copyfileobj(s, scores)
            for i in ['scores', 'kmers']:
                os.remove(join(outdir, f"{i}_{lower}_{upper}.b.gz"))
    
    return positions_dict


def run_index(genomes_input, outdir, split_memory=1, threads=1, index=None):
    k = 31
    if basename(outdir).endswith('.tar'):
        output_is_tar = True
        outdir = join(dirname(outdir), basename(outdir)[:-4])
    else:
        output_is_tar = False

    if isinstance(genomes_input, (tuple, list, set)):
        genomes = list(genomes_input)
        input_is_tar = False
    elif isfile(genomes_input) and tarfile.is_tarfile(genomes_input):
        input_is_tar = True
        with tarfile.open(genomes_input) as tar:
            genomes = [tarinfo.name for tarinfo in tar if tarinfo.isreg()]
    else:
        input_is_tar = False
        genomes = [join(
            genomes_input, file) for file in listdir(
            genomes_input)] if isdir(genomes_input) else genomes_input.split(',')
        genomes_string = ','.join(genomes)
        # Check if input files exist and are files
        for genome in genomes:
            if not exists(genome) or not isfile(genome):
                raise RuntimeError(f"{genome} does not exist or is not a file!")
                return 1

    # Make the output directory if it doesn't exist
    if not exists(outdir):
        mkdir(outdir)

    # Per genome set flags per kmer
    print_err("Indexing genomes.")
    post_dict, all_core_blocks = index_genomes(split_memory, genomes, outdir,
        threads, index, tar_file=(genomes_input if input_is_tar else ''))
    print_err("Finished Indexing.")

    print_err("Concatinating files.")
    positions_dictionary = concat_files(post_dict, all_core_blocks, outdir)
    print_err("Finished concatinating.")

    genomes_dict = {}
    for genome in genomes:
        genomes_dict[genome] = 0
        if input_is_tar:
            tar = tarfile.open(genomes_input)
            infile = gzip_agnostic_open(genome, 'rt', tar=tar)
        else:
            infile = gzip_agnostic_open(genome, 'rt')
        for record in SeqIO.parse(infile, 'fasta'):
            genomes_dict[genome] += len(str(record.seq))
        infile.close()
        if input_is_tar:
            tar.close()
    # if index != None:
    #     genomes, genomes_dict = update_genomes(index, genomes, genomes_dict)
        
    print_err("Saving metadata.")
    metadata_dict = {'kmer_size': k,
        'version': __version__,
        'genomes': {c:g for c, g in enumerate(genomes)},
        'genome_sizes': genomes_dict,
        'positions': positions_dictionary}
    with open(f'{outdir}/metadata.json', 'w') as outfile:
        json.dump(metadata_dict, outfile)
    if output_is_tar:
        with tarfile.open(f'{outdir}.tar', 'w') as tar:
            tar.add(outdir)
        shutil.rmtree(outdir)