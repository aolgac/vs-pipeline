# Glide Cross-Docking Optimization Pipeline

This directory contains the Glide-based cross-docking and evaluation workflow.
All steps are script-driven and configured via external .conf files.
No hard-coded paths, binding site information, or system-specific parameters are stored in the scripts.

## Environment

Activate the global environment once before running any step:

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

Script: 1_glide_prepare_receptors.py
Config: glide_receptor.conf

Prepares protein structures for Glide.

### 2. Prepare Ligands

Script: 2_glide_prepare_ligands.py
Config: glide_ligand.conf

Prepares ligand structures for docking.

### 3. Generate Grid Input Files

Script: 3_glide_generate_grid_inputs.py
Config: glide_grid.conf

Creates Glide grid input (.in) files.

### 4. Run Grid Generation

Script: 4_glide_run_grids.py
Config: glide_run.conf

Executes Glide grid generation jobs.

### 5. Cross-Docking

Script: 5_glide_crossdocking_runner.py
Config: glide_crossdock.conf

Runs Glide cross-docking.

### 6. Convert and Collect Poses

Script: 6_glide_convert_and_collect_poses.py
Config: glide_pose.conf

Converts docking outputs and collects ligand poses for analysis.

### 7. RMSD Calculation

Script: 7_glide_rmsd_pymol.py
Config: glide_rmsd.conf

Calculates RMSD between reference ligands and generated poses using PyMOL.

### 8. RMSD Matrix Construction

Script: 8_glide_rmsd_matrix_builder.py
Config: rmsd_matrix.conf

Builds an RMSD matrix from per-pose RMSD results.

### 9. RMSD Heatmap

Script: 9_glide_rmsd_heatmap.py
Config: heatmap.conf

Generates RMSD heatmaps for retrospective evaluation.

## Running the Full Pipeline

From the directory:

```bash
python run_glide_pipeline.py
```


The wrapper executes all steps sequentially using the corresponding configuration files.
