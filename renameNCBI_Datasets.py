#! /usr/bin/env python3

import pandas as pd
from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

"""
Abrir a pasta com os genomas do genbank baixados
abrir cada genoma para:
    renomear
    consequentemente escrever novamente o arquivo para funcionar no fastANI
"""

ncbi_path = Path("ncbi_dataset/ncbi_dataset/data/")

df = pd.read_csv(ncbi_path.joinpath("data_summary.tsv"), sep='\t')


for acc in df["Assembly Accession"]:
    print(acc)
    ass_name = df.loc[df["Assembly Accession"] == acc, ["Assembly Name"]].values.item()
    genome_name = df.loc[df["Assembly Accession"] == acc, ["Organism Scientific Name"]].values.item()

    records_list = []

    for record in SeqIO.parse(ncbi_path.joinpath(acc, f"{acc}_{ass_name.replace(' ', '_')}_genomic.fna"), "fasta"):
        
    #record = SeqIO.read(ncbi_path.joinpath(acc, f"{acc}_{ass_name}_genomic.fna"), "fasta")
        record_saida = SeqRecord(
            Seq(record.seq),
            id=record.id,
            description=record.description
        )
        records_list.append(record_saida)
    SeqIO.write(records_list, f"out_renamed/{genome_name.split()[0]}_{genome_name.split()[1]}.fasta", "fasta")
