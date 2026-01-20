# CompoundUniqifier

A tool to generate unique compound identifiers and organize chemical datasets. It converts SMILES to InChI and InChIKey, removes duplicates, and optionally merges with a reference dataset. Designed for downstream virtual screening. 

## Environment

Activate the global Conda environment before running any scripts:

```bash
conda activate vs-pipeline
```


## Running the Pipeline

1. Prepare dataset

Combine desired molecules obtained from Chemspace and Molport into a single CSV file with a SMILES column.

2. Generate unique compounds

```bash
python compound_uniqifier.py -i merged_dataset.csv -o uniqified.csv

```

3. Update an existing dataset (optional)
If you have a reference dataset and want to keep only compounds matching it:

```bash
python compound_uniqifier.py -i new_dataset.csv -o updated_dataset.csv -r reference_dataset.csv

```
### Arguments

* -i / --input : Path to the input CSV containing SMILES

* -o / --output : Path to the output CSV to save results

* -r / --reference : Optional path to a reference CSV to update the dataset
