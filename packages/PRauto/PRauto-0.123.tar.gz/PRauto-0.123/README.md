PRauto is a Bioinformatic and Chemoinformatics tool
that provides two main functionalities: Data Retrieval and Data Preprocessing.

To use the Data Retrieval feature, users can input the command "python -m prauto" into the command-line interface. This tool allows users to retrieve the FASTA file of a target protein sequence via a search query in the UniProt API. Additionally, using the UniProt accession number, PRauto retrieves the PDB files of target protein from the RCSB PDB API and sdf files of ligands that interact with the target protein from the ChEMBL API.

The output of this feature includes the target protein sequence in a FASTA file format, PDB files of the target protein structures, and sdf files of the ligands that interact with the target protein.

To use the Data Preprocessing feature, users can input the command "python -m prauto.prepauto" into the command-line interface. This tool processes PDB files that are located in a single directory. It extracts only the chain(s) that correspond to the target protein and aligns them according to the reference PDB file. It also removes any unnecessary molecules that are not involved in the binding of the primary ligand. In a PSE PyMOL session, these unnecessary molecules are hidden rather than being removed.

The output of this feature includes preprocessed PDB files and a PSE PyMOL session file
