#!/bin/python

import argparse
import commands
import multiprocessing
import numpy as np
import os
import pandas as pd
import re
import sys


def argument_parse():
    """Parsing arguments

    Args:
        None

    Returns:
        undet: undetermined fastq gz file
        
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
            '-u',
            '--undetermined',
            dest = 'undet',
            help = 'undetermined fastq file (gz compressed)',
            required = 'yes',
            )
    args = parser.parse_args()
    undet = args.undet
    return undet


def split_fastq(undet):
    """Split fastq file

    Split large undetermined fastq file into small chunks,
    and return them.
    
    Args:
        undet: undetermined fastq gz file

    Returns:
        fq_list: list of splitted small fastq files

    """

    pigz_test = commands.getstatusoutput('pigz -h')
    if pigz_test[0] == 0:
        pass
    else:
        print 'Error\t|\tpigz is not installed.'
        sys.exit()
    linux_split = commands.getstatusoutput('pigz -d -k -f -c ./{} | split -l 10000000 --additional-suffix=".fastq" '.format(undet))
    re_split_fq = 'x[a-z][a-z].fastq'
    fq_list = [f for f in os.listdir('./') if re.match(re_split_fq, f)]
    return fq_list


def read_undetermined(undeter_file):
    """Parsing index sequence and counting to make a dataframe

    Read undetermined fastq file line by line,
    and parse index sequence from the header line.
    Make a dataframe of index sequence and its count.

    Args:
        undet_file: undetermined file name

    Returns:
        index_df: a dataframe that has pairs of index sequence and its count
    
    """

    index_dict = {}
    line_num = 1
    with open(undeter_file, 'r') as rd_f:
        for line in rd_f:
            if line_num % 4 == 1:
                index = line.rstrip().split(':')[-1]
                if index in index_dict:
                    index_dict[index] += 1
                else:
                    index_dict[index] = 1
            line_num += 1
    index_df = pd.DataFrame(
            np.array(index_dict.values(), dtype=np.int),
            index = index_dict.keys(),
            columns = ['count']
            )
    return index_df


def multi_process(fq_list):
    """Analyze Undetermined fastq by multi-process

    Analyze splitted undetermined fastq using multi-process.
    Each process makes a dataframe that has a index sequence and its count.
    Finally all dataframes are merged into the one dataframe, called combined_df.

    """

    seed_num = len(fq_list)
    if seed_num > 50:
        seed_num = 50
    print 'Process\t|\tSeed number: {}'.format(str(seed_num))
    pool = multiprocessing.Pool(processes=seed_num)
    df_list = pool.map(read_undetermined, fq_list)
    pool.close()
    pool.join()
    combined_df = df_list[0]
    print 'Process\t|\tCombine {} data frames'.format(str(seed_num))
    if len(df_list) > 1:
        for sub_df in df_list[1:]:
            combined_df = combined_df.add(sub_df, fill_value=0)
    combined_df = combined_df.astype(int)
    return combined_df


def main():
    """ """
    undet = argument_parse()
    print 'Start\t|\tCheck incorrect index'
    fq_list = split_fastq(undet)

    print 'Process\t|\tAnalysis undetermined data'
    combined_df = multi_process(fq_list)
    sorted_combined_df = combined_df.sort_values(
            by='count',
            ascending=False,
            inplace=False
            )
    print sorted_combined_df.head(10)

    print 'Process\t|\tWrite out result'
    sorted_combined_df.to_csv('undetermined_top_index.csv', header=False)

    for f in fq_list:
        os.system('rm {}'.format(f))
        print 'End\t|\tCheck incorrect index'
        return True
    else:
        print 'End\t|\tCannot analyze index\n'
        return False

if __name__=='__main__':
    main()
