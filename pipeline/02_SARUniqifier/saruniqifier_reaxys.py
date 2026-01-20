#!/usr/bin/env python3
import os
import time
import argparse
import pandas as pd
from rdkit import Chem

def smiles_to_inchikey(smiles):
    if isinstance(smiles, str) and smiles.strip():
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            return Chem.inchi.MolToInchiKey(mol)
    return None

def main():
    parser = argparse.ArgumentParser(description="Reaxys SARUniqifier")
    parser.add_argument("-i", "--input_dir", required=True, help="Directory with input Excel files")
    parser.add_argument("-o", "--output_file", default="reaxys.csv", help="Output CSV file")
    args = parser.parse_args()

    input_files = [os.path.join(args.input_dir, f) for f in os.listdir(args.input_dir) if f.endswith('.xlsx')]
    if not input_files:
        print("No Excel files found.")
        return

    start_time = time.time()
    df = pd.concat([pd.read_excel(f) for f in input_files], ignore_index=True)

    columns_of_interest = [
        "SMILES", "Substance Identification: Reaxys Registry Number", "Target Transfection",
        "Substance Action on Target", "Substance Effect", "Bioassay Category", "Bioassay Name",
        "Bioassay Details", "Biological Species/NCBI ID", "(Clinical) findings / disease",
        "Organs/Tissues", "Cells/Cell Lines", "Cell Fraction", "Substance Dose",
        "Substance Route of Adm.", "Substance Dosing Regimen", "Measurement Object",
        "Medchem: Measurement Parameter", "Unit", "Qualitative value", "Quantitative value",
        "References"
    ]
    df = df[columns_of_interest].dropna(subset=['SMILES']).copy()
    df['Qualitative value'].fillna('=', inplace=True)
    df['InChI Key'] = df['SMILES'].apply(smiles_to_inchikey)
    df.insert(2, 'InChI Key - Main', df['InChI Key'].str[:14])
    df['key'] = df.groupby(['InChI Key - Main']).cumcount().astype(str)

    pivot_cols = [col for col in columns_of_interest if col != 'SMILES'] + ['SMILES']
    final = df.pivot_table(index='InChI Key - Main', columns='key', values=pivot_cols, aggfunc='first').sort_index(level=1, axis=1)
    final.columns = [''.join(col).replace('_','').replace(' ','') for col in final.columns.to_flat_index()]
    final.reset_index(inplace=True)
    final.to_csv(args.output_file, index=False)

    print(f"File '{args.output_file}' created in {time.time() - start_time:.3f} seconds.")

if __name__ == "__main__":
    main()
