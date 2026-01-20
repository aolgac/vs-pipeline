# SARUniqifier

SARUniqifier is a Python-based tool for organizing and consolidating bioactivity data from multiple sources. It processes datasets from Reaxys and ChEMBL, generates unique identifiers, and merges the data to create a unified dataset.

## Environment

Activate the global Conda environment before running any scripts:

```bash
conda activate vs-pipeline
```

## Running the Pipeline

1. reaxys_saruniqifier.py

Processes Reaxys Excel files:

```bash
python reaxys_saruniqifier.py -i path/to/reaxys_files/ -o reaxys.csv
```

* -i: Input directory containing Reaxys .xlsx files

* -o: Output CSV file

2. chembl_saruniqifier.py

Fetches and processes ChEMBL activity data:

```bash
python chembl_saruniqifier.py -t CHEMBL_ID -o chembl.csv
```

* -t: ChEMBL target ID

* -o: Output CSV file

3. saruniqifier_merge.py

Merges Reaxys and ChEMBL datasets:

```bash
python saruniqifier_merge.py -r reaxys.csv -c chembl.csv -o merged.csv
```

* -r: Reaxys CSV file

* -c: ChEMBL CSV file

* -o: Output merged CSV file