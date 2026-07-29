#!/usr/bin/python4

from gprofiler import GProfiler
from collections import Counter
import fileinput, os, sys


gp = GProfiler(return_dataframe = False)

# converts gene ids and culls for gene interactions above cutoff
def convertGeneID(location, edge_cutoff):
    translations = {}
    with fileinput.input(files=location, inplace=True) as file:
        for line in file:
            line = line.split()
            if float(line[-1]) >= edge_cutoff:
                for gene in line[:-1]:
                    if gene in translations:
                        print(f'{translations[gene]}\t', end = '')
                    else:
                        gene_info = gp.convert(query = gene, organism = 'hsapiens', numeric_namespace = "ENTREZGENE_ACC")
                        name = gene_info[0]['name']
                        translations[gene] = name
                        print(f'{name}\t', end = '')
                print(line[-1])
    return list(translations.values())
                
#generates connectivity file
def connectivity(network_file):
    with open(network_file, encoding="utf-8") as data:
        list_genes = data.read().split()
        del(list_genes[2::3])
    freq = dict(Counter(list_genes))
    
    filename = 'Data_NHC_Network_Connectivity.txt'
    
    genes = list(freq.keys())
    with open(filename, 'w') as conn_file:
        for gene in genes:
            conn_file.write(f'{gene}\t{freq[gene]}\n')


def generateNetwork(network_file, edge_cutoff):
    convertGeneID(network_file, edge_cutoff)
    connectivity(network_file)
    os.rename(network_file, 'Data_NHC_Network.txt')

generateNetwork(sys.argv[1], float(sys.argv[2]))
