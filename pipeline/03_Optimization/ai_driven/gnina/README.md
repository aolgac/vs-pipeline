# GNINA Cross-Docking Optimization Pipeline

This directory contains scripts for performing GNINA cross-docking, extracting the first ligand pose, calculating RMSD, building RMSD matrices, and generating heatmaps. Each script uses its own `.conf` file for configuration.

## Environment

Activate the global Conda environment before running any scripts:

```bash
conda activate vs-pipeline
```

## Pipeline Overview
### 1. Cross-Docking

Script: 1_gnina_crossdock.py
Config: gnina_crossdock.conf

Performs cross-docking for all receptor-ligand pairs using GNINA. Outputs docked ligand poses in .sdf format.

### 2. Extract First Pose

Script: 2_extract_first_pose.py
Config: gnina_extract_first_pose.conf

Extracts the first docking pose from each GNINA output .sdf file. Saves the first pose in a separate folder.

### 3. RMSD Calculation

Script: 3_gnina_rmsd.py
Config: gnina_rmsd.conf

Computes RMSD between reference ligands and generated docking poses using PyMOL.

### 4. RMSD Matrix Builder

Script: 4_gnina_rmsd_matrix.py
Config: gnina_rmsd_matrix.conf

Builds a reference vs. target RMSD matrix from the results of RMSD calculations.

### 5. Heatmap Visualization

Script: 5_gnina_rmsd_heatmap.py
Config: gnina_heatmap.conf

Generates a heatmap figure of the RMSD matrix for visual analysis.

## Running the Pipeline

Use the wrapper script to execute all steps sequentially:

```bash
python run_gnina_pipeline.py
```

This will run scripts 1 → 2 → 3 → 4 → 5 in order, using their respective .conf files.


Make sure all .conf files point to the correct input/output directories and parameters before running the pipeline.
