# Vina Cross-Docking Optimization Pipeline

This directory contains scripts for preparing receptors and ligands, running Vina cross-docking, calculating RMSD, building matrices, and generating heatmaps. Each script uses its own .conf file for configuration.

## Environment

Activate the global Conda environment before running any scripts:

```bash
conda activate vs-pipeline
```

## Configuration
Configuration

Each script reads its parameters from a dedicated .conf file located in config/.

Before execution:

cp config/*.conf.example config/*.conf


Edit the copied .conf files according to your local setup and data layout.

## Pipeline Overview
### 1. Prepare Receptors

Script: 1_prepare_receptors_pdb_to_pdbqt.py

Config: vina_receptor.conf

Converts PDB proteins to PDBQT for docking.

### 2. Convert Ligands

Script: 2_convert_ligands_mae_to_pdbqt.py

Config: vina_ligand.conf

Converts .mae ligands to PDBQT through Mol2 intermediate.

### 3. Run Vina Docking

Script: 3_run_vina_crossdocking.py

Config: vina_docking.conf

Executes cross-docking for all receptor-ligand pairs.

### 4. Extract Model 1

Script: 4_extract_vina_model1.py

Config: model1_extraction.conf

Extracts the first docking pose from each output PDBQT.

### 5. RMSD Calculation

Script: 5_vina_rmsd_pymol.py

Config: vina_rmsd.conf

Computes RMSD between reference ligands and generated poses.

### 6. RMSD Matrix Builder

Script: 6_vina_rmsd_matrix_builder.py

Config: rmsd_matrix.conf

Builds a reference vs. target RMSD matrix.

### 7. Heatmap Visualization

Script: 7_vina_rmsd_heatmap.py

Config: heatmap.conf

Generates a heatmap figure of the RMSD matrix.

## Running the Pipeline

Use the wrapper script to execute all steps sequentially:

```bash
python run_vina_pipeline.py
```

Make sure all .conf files point to the correct input/output directories and parameters.