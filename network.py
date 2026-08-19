from gprofiler import GProfiler
from collections import Counter
import fileinput, os, sys
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
#utils = importr('utils')

#utils.install_packages('org.Hs.eg.db')
importr('org.Hs.eg.db')

gp = GProfiler(return_dataframe = False)

# converts gene ids and culls for gene interactions above cutoff
def convertGeneID(location, edge_cutoff):
    translations = {}
    with fileinput.input(files=location, inplace=True) as file:
        for line in file:
            line = line.split()
            if float(line[-1]) >= edge_cutoff:
                converted_line = []

                for gene in line[:-1]:
                    if gene in translations:
                        name = translations[gene]
                    else:
                        try:
                            name = ro.r(f'mapIds(org.Hs.eg.db, keys = c("{gene}"), column = "SYMBOL", keytype = "ENTREZID")')[0]
                            translations[gene] = name
                        except:
                            try:
                                gene_info = gp.convert(query = gene, organism = 'hsapiens', numeric_namespace = "ENTREZGENE_ACC")
                                name = gene_info[0]['name']
                                translations[gene] = name
                            except:
                                name = "None"
                    converted_line.append(name)

                if 'None' not in converted_line:
                    print(f'{converted_line[0]}\t{converted_line[1]}\t{line[-1]}')
    return list(translations.values())

#generates connectivity file
def connectivity(network_file):
    with open(network_file, encoding="utf-8") as data:
        list_genes = data.read().split()
        del(list_genes[2::3])
    freq = dict(Counter(list_genes))

    filename = f'Connectivity_{network_file}.txt'

    genes = list(freq.keys())
    with open(filename, 'w') as conn_file:
        for gene in genes:
            conn_file.write(f'{gene}\t{freq[gene]}\n')


def generateNetwork(network_file, edge_cutoff):
    convertGeneID(network_file, edge_cutoff)
    connectivity(network_file)
    os.rename(network_file, f'Network_{network_file}.txt')

def genNetworkFromList(folder, edge_cutoff):
    files = os.listdir(os.path.expanduser(folder))
    for file in files:
        if file[-4:] == "_top":
            generateNetwork(file, edge_cutoff)

#generateNetwork(sys.argv[1], float(sys.argv[2]))
genNetworkFromList(sys.argv[1], float(sys.argv[2]))
