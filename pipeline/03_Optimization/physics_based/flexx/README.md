# FlexX Cross-Docking Optimization Pipeline

This directory contains the FlexX-based cross-docking and evaluation workflow.
All steps are script-driven and configured via external `.conf` files.

## Environment

Activate the global environment once before running any step:

```bash
conda activate vs-pipeline
```

## Configuration

Each script reads its parameters from a dedicated `.conf` file located in `configs/`.

Before execution:

cp configs/*.conf.example configs/*.conf

Edit the copied `.conf` files according to your local setup and data layout.

## Pipeline Overview

### 1. Cross-Docking

Script: 1_run_flexx_crossdocking.py  
Config: flexx_crossdock.conf  

Runs FlexX cross-docking using a ligand pool and protein set, with reference ligand matching.

### 2. Split Docked SDF Files

Script: 2_split_flexx_sdf.py  
Config: flexx_split.conf  

Splits multi-molecule SDF outputs into individual ligand files.

### 3. RMSD Calculation

Script: 3_flexx_rmsd_pymol.py  
Config: flexx_rmsd.conf  

Calculates RMSD between reference ligands and docked poses using PyMOL.

### 4. RMSD Matrix Construction

Script: 4_flexx_rmsd_matrix_builder.py  
Config: flexx_rmsd_matrix.conf  

Builds a reference × target RMSD matrix.

### 5. RMSD Heatmap

Script: 5_flexx_rmsd_heatmap.py  
Config: flexx_heatmap.conf  

Generates RMSD heatmaps for retrospective evaluation.

## Running the Full Pipeline

From the FlexX directory:

```bash
python run_flexx_pipeline.py
```

The wrapper executes all steps sequentially using the corresponding configuration files.

