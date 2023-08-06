#!/usr/bin/env python

from .retriever.get_fasta import *
from .retriever.get_pdb import *
from .retriever.get_ligand import *
from tqdm.auto import tqdm
from tkinter import Tk
from tkinter import filedialog

root = Tk()
root.withdraw()

mult = '\n' * 3
global search_key


def main():
    global search_key
    target_dir = filedialog.askdirectory(title='Select a directory to work with')
    os.chdir(target_dir)
    print(f'Step1: Retrieve FASTA files{mult}')
    print(f"""
    
########################################################################################################

 > Please input [ Protein Name ] and [ Gene Name ] of your target.


    input 1  Protein Name with subtype :  ex. 5-hydroxytryptamine receptor 2A   
                                                                             / Search term(uniprot API)
                                                                               
    input 2  Gene Name :  ex. HTR2A                                 
                                     / Filtering term for Integrity of data 
                                                  
#########################################################################################################
                                                                                            """)
    search_key = input('input 1  Protein Name with subtype :')
    gene_name = input('input 2  Gene Name :')
    dir_name = input('input Directory Name for FASTA file: ')
    fasta_file_path = download_fasta(search_key, dir_name)
    fasta_file_path = remove_outlier(search_key,gene_name,fasta_file_path)
    pdb_dir = os.path.dirname(fasta_file_path)

    print(f'Step2: Retrieve PDB files{mult}')
    accessions_list = extract_accessions(fasta_file_path)
    for accession in accessions_list:
        pdb_ids = search_pdb_by_accession(accession)
        if pdb_ids:
            print(f'\nFound {len(pdb_ids)} PDB entries for {accession}')
            download_pdb_files_by_acc(pdb_ids, accession, pdb_dir)

    for accession in tqdm(accessions_list, total=len(accessions_list), desc='Searching Ligands'):
        download_chembl_compounds(accession, pdb_dir)


if __name__ == "__main__":
    main()