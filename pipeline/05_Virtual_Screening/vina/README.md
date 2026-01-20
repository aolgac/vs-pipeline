# Vina Cross-Docking Pipeline

This repository contains a fully automated Vina-based virtual screening pipeline designed to process large ligand libraries, convert molecular formats, and perform docking calculations against target proteins. The pipeline supports checkpoints, parallel processing, and structured logging.

## Overview

The Vina pipeline automates the following tasks:

Molecule Extraction – Extracts individual molecules from .mae files based on a reference CSV containing ligand names.

Format Conversion – Conyverts .mae → .mol2 → .pdbqt for compatibility with AutoDock Vina.

Docking – Performs ligand docking against prepared protein structures using Vina.

Checkpoints and Logging – Tracks progress to allow resuming and monitors errors and progress.

This workflow is optimized for high-throughput virtual screening with large ligand libraries.

## Pipeline Workflow

The pipeline consists of four main stages:

1. Molecule Extraction

Extracts ligands listed in a CSV from .mae files.

Creates individual .mae files for each molecule.

File naming convention: <vs_context>_<molecule_name>.mae.

Uses checkpoints to skip molecules already extracted.

2. .mae → .mol2 Conversion

Converts extracted .mae files to .mol2 using Schrödinger’s structconvert.py.

Each conversion creates a checkpoint to avoid redundant processing.

3. .mol2 → .pdbqt Conversion

Converts .mol2 files into .pdbqt format using MGLTools AutoDockTools (prepare_ligand4.py).

Required for docking with AutoDock Vina.

4. Docking

Iterates over all proteins and ligands, generating a docking output for every pair.

Uses the grid box coordinates from the configuration file (center_x, center_y, center_z, size_x, size_y, size_z).

Docking outputs: <protein_name>_<ligand_name>.pdbqt.

Parallelized using Python multiprocessing for efficiency.

## Configuration

The pipeline is controlled by a JSON configuration file (config.json).

Example structure:

```bash
{
{
    "log_dir": "/path/to/logs",
    "csv_file": "/path/to/ligand_list.csv",
    "mae_dir": "/path/to/mae_files",
    "extracted_mae_dir": "/path/to/extracted_mae",
    "mol2_output_dir": "/path/to/mol2",
    "pdbqt_output_dir": "/path/to/pdbqt",
    "protein_dir": "/path/to/proteins",
    "docking_output_dir": "/path/to/docking_results",
    "checkpoints_dir": "/path/to/checkpoints",
    "vina_path": "./vina",
    "mgltools_path": "/path/to/MGLTools",
    "grid_box": {
        "center_x": 0,
        "center_y": 0,
        "center_z": 0,
        "size_x": 20,
        "size_y": 20,
        "size_z": 20
    },
    "num_cpus": 56
}
```

Key Fields:

```bash
log_dir: Where pipeline logs are stored.

csv_file: CSV containing ligand names for extraction.

mae_dir: Directory containing source .mae ligand files.

extracted_mae_dir: Directory for individual extracted .mae molecules.

mol2_output_dir: Directory for .mol2 conversion outputs.

pdbqt_output_dir: Directory for .pdbqt files.

protein_dir: Directory containing prepared protein .pdbqt files.

docking_output_dir: Directory for docking results.

checkpoints_dir: Directory storing checkpoints for each step.

vina_path: Path to Vina executable.

mgltools_path: Path to MGLTools installation.

grid_box: Coordinates and dimensions of the docking box.

num_cpus: Number of CPUs for parallel processing.
```

## Logging and Checkpoints

Logs are written to log_dir/docking_process.log.

Checkpoints prevent recomputation and allow the pipeline to resume after interruptions.

Each major step (extraction, conversion, docking) creates a .chk file in checkpoints_dir for each molecule or docking pair.

## Running the Pipeline

1. Prepare the configuration file (config.json).

2. Ensure all directories exist or are specified in the config.

3. Activate the vs environment.

```bash
conda activate vs-pipeline
```

4. Run the pipeline:

```bash
python vina_pipeline.py --config config.json
```

The pipeline will process all ligands in parallel and generate .pdbqt docking outputs for each protein-ligand pair.

## Notes

- Make sure the grid box coordinates correctly cover the binding site.

- .mae files must match the ligand names listed in the CSV.

- Schrödinger structconvert.py must be accessible in the specified path.

- MGLTools must be properly installed for .pdbqt conversion.

- The pipeline is scalable to thousands of ligands and proteins with proper CPU allocation.