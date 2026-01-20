#!/usr/bin/env python3
import time
import argparse
import pandas as pd
from rdkit import Chem
from chembl_webresource_client.new_client import new_client

def smiles_to_inchikey(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        return Chem.inchi.MolToInchiKey(mol)
    return None

def rename_columns(col_name):
    return col_name.replace('_', ' ').title()

def main():
    parser = argparse.ArgumentParser(description="ChEMBL SARUniqifier")
    parser.add_argument("-t", "--target_chembl_id", required=True, help="ChEMBL target ID")
    parser.add_argument("-o", "--output_file", default="chembl.csv", help="Output CSV file")
    args = parser.parse_args()

    start_time = time.time()

    activities = new_client.activity.filter(target_chembl_id__in=[args.target_chembl_id])
    chembl = pd.DataFrame(activities)
    chembl.columns = [rename_columns(c) for c in chembl.columns]
    chembl.dropna(subset=['Canonical Smiles'], inplace=True)
    chembl.reset_index(drop=True, inplace=True)
    chembl['Standard Relation'].fillna('=', inplace=True)
    chembl['InChIKey'] = chembl['Canonical Smiles'].apply(smiles_to_inchikey)
    chembl.insert(1, 'InChI Key - Main', chembl['InChIKey'].str[:14])
    chembl['References'] = (
        chembl['Src Id'].astype(str) + ' (' +
        chembl['Document Year'].astype(str) + ') | ' +
        chembl['Document Journal'] + ' | ' +
        chembl['Document Chembl Id'].astype(str)
    )

    drop_cols = [
        'Action Type','Activity Id','Assay Chembl Id','Bao Endpoint','Bao Format',
        'Data Validity Description','Document Chembl Id','Document Journal','Document Year',
        'Molecule Pref Name','Parent Molecule Chembl Id','Pchembl Value','Potential Duplicate',
        'Qudt Units','Record Id','Src Id','Standard Flag','Standard Text Value',
        'Standard Upper Value','Target Chembl Id','Target Organism','Target Pref Name',
        'Target Tax Id','Text Value','Toid','Type','Upper Value'
    ]
    chembl.drop(columns=drop_cols, inplace=True)

    groups = chembl.groupby('InChI Key - Main')
    new_rows = []

    for _, group in groups:
        new_row = group.iloc[0].copy()
        for i in range(1, len(group)):
            row = group.iloc[i]
            row.index = [f'{col}_{i}' for col in row.index]
            new_row = pd.concat([new_row, row])
        new_rows.append(new_row)

    new_chembl = pd.DataFrame(new_rows)
    new_chembl.reset_index(drop=True, inplace=True)
    new_chembl.to_csv(args.output_file, index=False)

    print(f"File '{args.output_file}' created for ChEMBL target {args.target_chembl_id} in {time.time() - start_time:.3f} seconds.")

if __name__ == "__main__":
    main()
