import argparse
import pandas as pd


from settings import cols2use, ASSEMBLY_SUM, ASSEMBLY_LEVELS


def read_assembly_summary(Path2file: str) -> pd.DataFrame:
    df = pd.read_csv(Path2file, sep="\t", header=1, usecols=cols2use)
    df["seq_rel_date"] = pd.to_datetime(df["seq_rel_date"], format='%Y/%m/%d')
    return df

# Primeiro filtro é por espécie, argumento vem do argparse
def species_filter(all_species_df: pd.DataFrame) -> pd.DataFrame:
    x = all_species_df.loc[df["organism_name"] == "Bacillus velezensis"]
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
    print(date_filtered)


if __name__ == '__main__':
    #def handle_command(command):
    #    match command:
#            case [args.species]:
#                species = species_filter(df)
#            case [args.species, args.assembly]:
#                species = species_filter(df)
#                ASSEMBLY_LEVELS.remove(args.assembly)
#                assemblies = assembly_level_filter(species)
#            case [args.species, args.date_filter]:
#                species = species_filter(df)
#                upload_data_filter(assemblies, "2020/01/01")
#            case [args.species, args.assembly, args.date_filter]:
#                species = species_filter(df)
#                ASSEMBLY_LEVELS.remove(args.assembly)
#                assemblies = assembly_level_filter(species)
#                upload_data_filter(assemblies, "2020/01/01")


    parser = argparse.ArgumentParser()
    parser.add_argument('-sp', '--species', help="Genus and species from wanted organism.")
    parser.add_argument('-l', '--level', help="Assemble level to remove from download list.")
    parser.add_argument('-d', '--date', help="Date to filter downloads, use YY/MM/DD pattern.")
    args = parser.parse_args()
    print(args)


    #df = read_assembly_summary(ASSEMBLY_SUM)
    #species = species_filter(df)
    #ASSEMBLY_LEVELS.remove('Contig')
    ## ASSEMBLY_LEVELS.remove('item do argparse'), precisa fazer isso antes de rodar o filtro caso tenha q tirar genomas com montagem de nivel menor 
    #assemblies = assembly_level_filter(species)
    #upload_data_filter(assemblies, "2020/01/01")

