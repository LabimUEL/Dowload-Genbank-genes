cols2use = ["#assembly_accession", "organism_name", "assembly_level", "genome_rep", "seq_rel_date", "ftp_path"]

ASSEMBLY_SUM = "/media/labim/HDD/Documentos/assembly_summary_genbank.txt"

ASSEMBLY_LEVELS = {"Contig", "Scaffold", "Complete Genome", "Chromosome"}

HEADER = """
=================================================================
======= LABIM - Laboratório de Biotecnologia Microbiana =========
=================================================================
Programa para baixar genomas do Genbank/NCBI através da tabela
assembly_summary_genbank.txt.

https://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_genbank.txt

A espécie é obrigatório ser passado para selecionar genomas.
"""
