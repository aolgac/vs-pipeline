# DiffDock Cross-Docking Optimization Pipeline

This directory contains scripts for generating protein-ligand CSVs, running DiffDock inference, collecting top-ranked poses, calculating RMSD, building matrices, and generating heatmaps. Each script uses its own `.conf` file for configuration.

## Environment

Activate the global Conda environment before running any scripts:

```bash
conda activate vs-pipeline
```

## Pipeline Overview
### 1. Generate DiffDock CSV

Script: 1_generate_diffdock_csv.py
Config: diffdock_filepaths.conf.py
Generates a CSV file containing all protein-ligand combinations for DiffDock inference.

### 2. Run DiffDock Inference

Script: 2_run_diffdock_inference.py
Config: diffdock_inference.conf.py
Runs DiffDock inference to produce predicted ligand poses.

### 3. Collect Rank1 Poses

Script: 3_collect_diffdock_rank1.py
Config: diffdock_collect.conf.py
Collects the top-ranked (rank1.sdf) poses from all output directories into a single folder.

### 4. RMSD Calculation

Script: 4_diffdock_rmsd_pymol.py
Config: diffdock_rmsd.conf.py
Computes RMSD values between reference ligands and predicted poses using PyMOL.

### 5. RMSD Matrix Builder

Script: 5_diffdock_rmsd_matrix_builder.py
Config: diffdock_rmsd_matrix.conf.py
Constructs a reference vs. target RMSD matrix from per-pose RMSD results.

### 6. RMSD Heatmap

Script: 6_diffdock_rmsd_heatmap.py
Config: diffdock_heatmap.conf.py
Generates a heatmap visualization of the RMSD matrix.

##Running the Pipeline

Use the wrapper script to execute all steps sequentially:

```bash
python run_vina_pipeline.py
```


Make sure all .conf files point to the correct input/output directories and parameters.
