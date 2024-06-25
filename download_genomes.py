import argparse
import subprocess
import pandas as pd
import numpy as np

from pathlib import Path
from typing import List, Union, Dict


from settings import cols2use, ASSEMBLY_SUM, ASSEMBLY_LEVELS, HEADER, suffixes


def read_assembly_summary(Path2file: str) -> pd.DataFrame:
    df = pd.read_csv(Path2file, sep="\t", header=1, usecols=cols2use)
    df["seq_rel_date"] = pd.to_datetime(df["seq_rel_date"], format='%Y/%m/%d')
    return df

# Primeiro filtro é por espécie, argumento vem do argparse
def species_filter(all_species_df: pd.DataFrame, sp_name: str) -> pd.DataFrame:
    x = all_species_df.loc[df["organism_name"] == sp_name]
    #print(x)
    return x

# Segundo filtro é de nível de montagem
def assembly_level_filter(species_df: pd.DataFrame) -> pd.DataFrame:
    y = species_df[species_df["assembly_level"].isin(ASSEMBLY_LEVELS)]
    #print(y)
    return(y)
    

def upload_data_filter(assemblies_df: pd.DataFrame, date_filter: str) -> None:
    filter_date = pd.to_datetime(date_filter)
    date_filtered = assemblies_df[assemblies_df["seq_rel_date"] > filter_date]
    return date_filtered

def create_download_link_list(ftp_paths: pd.Series, sufix: Union[str, List]) -> list:
    link_struct = dict()

    if isinstance(sufix, str):
        link_struct["suffixes"] = [suffixes[sufix]]
    if isinstance(sufix, List):
        link_struct["suffixes"] = [suffixes[suf] for suf in sufix]

    link_struct["preffixes"] = list()
    raw_link_list = list()

    for link in ftp_paths:
        raw_link_list.append(f'{link}/{link.split("/")[-1]}_')
    link_struct["preffixes"].extend(raw_link_list)

    results_list = [pref + suff for pref in link_struct["preffixes"] for suff in link_struct["suffixes"]]

    return results_list

def execute_download(files_list: List, outpath: str, count: int, ref_df: pd.DataFrame) -> None:

    real_count = 0
    for file_ in files_list:
        #https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/855/275/GCA_003855275.1_ASM385527v1/GCA_003855275.1_ASM385527v1_cds_from_genomic.fna.g
        acc = "_".join(file_.split("/")[-1].split("_")[0:2])
        print(acc)
        org_name = ref_df.loc[ref_df["#assembly_accession"] == acc, "organism_name"].values[0]
        isolate = ref_df.loc[ref_df["#assembly_accession"] == acc, "isolate"]
        print(isolate)
        print(type(isolate))
        print()
        #if pd.isna(ref_df.loc[ref_df["#assembly_accession"] == acc, "isolate"]):
        if isolate.empty:
            print(f"isolate is NA -> {isolate}")

        #isolate = ref_df.loc[ref_df["#assembly_accession"] == acc, "infraspecific_name"].values[0]

        print(org_name, isolate)
        break
        try:
            Path(f"{outpath}/{acc}").mkdir()
        except FileExistsError:
            pass
        cmd = subprocess.Popen([f"wget {file_} -P {outpath}/{acc} --tries 3 --show-progress --output-file={outpath}/{acc}/file.log"], shell=True, encoding="UTF-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        outs, errs = cmd.communicate()
        
        print(f"====>>> OUTS\n{outs}")
        print(f"====>>> ERRS\n{errs}")

        real_count = real_count + 1
        if real_count == count:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=HEADER, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('species', type=str, help="Genus and species from wanted organism.")
    parser.add_argument('-l', '--level', choices=ASSEMBLY_LEVELS, help="Assembly level to remove from download list.")
    parser.add_argument('-d', '--date', help="Date to filter downloads, use YYYY/MM/DD pattern.")
    parser.add_argument('-f', '--files', type=str, nargs='+', help="Files to download", default="genome_fasta")
    parser.add_argument('-o', '--output-path', type=str, help="Absolute path to output location")
    args = parser.parse_args()
    print(args)

    # Namespace(date=None, level=None, species='Klebsiella pneumoniae')

    #data, level, sp_ = vars(args)

    level = args.level
    sp_ = args.species
    data = args.date
    files = args.files
    output = args.output_path

    #print(data, level, sp_)
    
    df = read_assembly_summary(ASSEMBLY_SUM)
    df = df.replace('na', np.nan)

    species = species_filter(df, sp_)

    if level and isinstance(data, None):
        ASSEMBLY_LEVELS.remove(level)
        assemblies = assembly_level_filter(species)
        print(assemblies)
    elif data and isinstance(level, None):
        date_filt = upload_data_filter(species, "2020/01/01")
        print(date_filt)
    elif level and data:
        ASSEMBLY_LEVELS.remove(args.assembly)
        assemblies = assembly_level_filter(species)
        fully_filt = upload_data_filter(assemblies, "2020/01/01")
        print(fully_filt)
    else:
        print(species)
        print()
        list2download = create_download_link_list(species["ftp_path"], files)
        execute_download(list2download, output, 10, species)
        
    

    #df = read_assembly_summary(ASSEMBLY_SUM)
    #species = species_filter(df)
    #ASSEMBLY_LEVELS.remove('Contig')
    ## ASSEMBLY_LEVELS.remove('item do argparse'), precisa fazer isso antes de rodar o filtro caso tenha q tirar genomas com montagem de nivel menor 
    #assemblies = assembly_level_filter(species)
    #upload_data_filter(assemblies, "2020/01/01")

