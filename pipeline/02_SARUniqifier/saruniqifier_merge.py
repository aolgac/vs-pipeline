#!/usr/bin/env python3
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Merge Reaxys and ChEMBL SAR datasets")
    parser.add_argument("-r", "--reaxys_file", required=True, help="Input Reaxys CSV file")
    parser.add_argument("-c", "--chembl_file", required=True, help="Input ChEMBL CSV file")
    parser.add_argument("-o", "--output_file", default="merged_sar.csv", help="Output merged CSV file")
    args = parser.parse_args()

    reaxys_df = pd.read_csv(args.reaxys_file)
    chembl_df = pd.read_csv(args.chembl_file)
    merged_df = pd.merge(reaxys_df, chembl_df, on='InChI Key - Main', how='outer')
    merged_df.to_csv(args.output_file, index=False)
    print(f"File '{args.output_file}' created. Total rows: {len(merged_df)}")

if __name__ == "__main__":
    main()
