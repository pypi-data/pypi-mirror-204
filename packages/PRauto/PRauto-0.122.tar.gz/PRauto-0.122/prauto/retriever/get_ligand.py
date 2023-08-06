#!/usr/bin/env python

import os
from chembl_webresource_client.settings import Settings
from chembl_webresource_client.new_client import new_client
from functools import lru_cache
from tqdm import tqdm


Settings.Instance().CACHING = True
@lru_cache(maxsize=128)
def download_chembl_compounds(accession,save_path):

    # Create the "ligands" directory if it does not exist
    if not os.path.exists(os.path.join(save_path, "ligands")):
        os.makedirs(os.path.join(save_path, "ligands"))

    targets_api = new_client.target
    compounds_api = new_client.molecule
    bioactivities_api = new_client.activity

    targets = targets_api.get(target_components__accession=accession,
                              target_type__in=['SINGLE PROTEIN','PROTEIN FAMILY']).only("target_chembl_id")
    targets_id = list(set([target['target_chembl_id'] for target in targets]))

    if len(targets_id) != 0:

        target_columns_list = ["molecule_chembl_id", "standard_value", "target_chembl_id"]
        try:
            for target in targets_id:

                bioactivities = bioactivities_api.filter(target_chembl_id=target, standard_type="IC50",
                                                      assay_type__in=["B","F"],relation__in=['=', '<', '<='],
                                                      **{f"activity_IC50__isnull": False}).only(
                    *target_columns_list)

                compound_columns_list = ["molecule_chembl_id", 'molecule_structures']
                compounds = compounds_api.filter(
                    molecule_chembl_id__in=[x['molecule_chembl_id'] for x in bioactivities],
                    molecule_properties__mw_freebase__lte=700).only(*compound_columns_list)

                compounds_list = [record for record in compounds]

                if len(compounds_list) != 0:
                    # Iterate through the list and save each molecule as a .pdb file
                    for record in tqdm(compounds_list,total=len(compounds_list),desc='Retrieving Molecules'):
                        mol_id = record['molecule_chembl_id']
                        file_name = f"{mol_id}_{accession}.sdf"
                        file_path = os.path.join(save_path, "ligands", file_name)
                        if os.path.exists(file_path):
                            continue
                        mol_file = record['molecule_structures']['molfile']
                        with open(file_path, 'w') as outfile:
                            outfile.write(mol_file)

        except Exception as e:
            print(f"Failed to download ligands associated with {target}: {e}")