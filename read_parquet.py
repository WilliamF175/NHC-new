import pyarrow.parquet as pq
from gprofiler import GProfiler
import os, sys

gp = GProfiler(return_dataframe = False)

def parquet_listing(folder):
    all_files = os.listdir(os.path.expanduser(folder))
    parquets = []
    for file in all_files:
        if file.find('.snappy.parquet') != -1:
            parquets.append(f'{folder}{file}')
    print('done successfully')
    return parquets


def schema_list(filename):
    schema = str(pq.ParquetFile(filename).schema_arrow).split('\n')

    column = 0
    while column < len(schema):
        schema[column] = schema[column][:schema[column].find(':')]
        column += 1
    return schema[:-3]

def parquet_to_tsv(filename, output_name, columns):
    table = pq.read_table(os.path.expanduser(filename), columns=columns).to_pandas()
    keys = list(table.keys())
    with open(os.path.expanduser(output_name), 'a', encoding = 'utf-8') as file:
        index = 0
        while index < len(table):
            for key in keys:
                file.write(f'{table[key][index]}\t')
                del(table[key][index])
            file.write('\n')
            index += 1
    del(table)
    print('nothing blew up')

def folder_to_tsv(folder, output_path):
    parquets = parquet_listing(folder)
    schema = schema_list(parquets[0])

    columns = []
    for column in schema:
        choice = input(f'keep column {column}?\ny or n\n')
        if choice == 'y':
            columns.append(column)
    print(columns)

    for parquet in parquets:
        parquet_to_tsv(parquet, output_path, columns)

if __name__ == "__main__":
    folder_to_tsv(sys.argv[1], sys.argv[2])
