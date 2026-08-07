import pyarrow.parquet as pq
import pandas as pd
import numpy as np
import os

def merge_parquets(folder, output_name):
    all_files = os.listdir(os.path.expanduser(folder))
    parquets = []
    for file in all_files:
        if file.find('.snappy.parquet') != -1:
            parquets.append(f'{folder}{file}')
            
    schema = pq.ParquetFile(parquets[0]).schema_arrow
    with pq.ParquetWriter(os.path.expanduser(output_name), schema=schema) as writer:
        for file in parquets:
            writer.write_table(pq.read_table(os.path.expanduser(file), schema=schema))
    print('done successfully')

def parquet_to_tsv(filename, output_name):
    table = pq.read_table(os.path.expanduser(filename)).to_pandas()
    keys = list(table.keys())
    with open(os.path.expanduser(output_name), 'x', encoding = 'utf-8') as file:
        index = 0
        while index < len(table):
            for key in keys:
                file.write(f'{table[key][index]}\t')
                del(table[key][index])
            file.write('\n')
            index += 1
    del(table)
    print('nothing blew up')