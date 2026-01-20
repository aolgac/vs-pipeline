# FlexX Virtual Screening Pipeline

This repository contains a fully automated FlexX-based virtual screening pipeline designed to process large ligand libraries, convert MAE ligands to SDF, run FlexX docking, and process docking outputs. The pipeline supports checkpoints, sequential step execution, and structured logging.

## Overview

The FlexX pipeline automates the following tasks:

MAE → SDF Conversion & Merging – Converts MAE ligands to SDF and merges them into a single SDF library.

Docking with FlexX – Performs docking against a prepared protein using a reference ligand.

Post-Docking Processing – Filters the top poses (_01), extracts docking scores, and saves individual SDFs and a CSV summary.

Checkpoints & Logging – Tracks progress and allows the pipeline to resume after interruptions.

This workflow is optimized for high-throughput virtual screening with large ligand libraries.

## Pipeline Workflow

The pipeline consists of three main steps:

**1. Step 1** – Convert MAE to SDF and Merge

Converts ligands from input_mae_dir into individual SDF files in output_sdf_dir.

Merges all SDFs into a single file merged_sdf_path.

Checkpoints: mae_to_sdf_vs_run.chk, merge_sdf_vs_run.chk.

**2. Step 2** – Run FlexX Docking

Uses the merged SDF as input.

Runs docking with the specified protein (protein_path) and reference ligand (reference_ligand).

Saves docked poses to docking_output_sdf_name in output_base_dir.

Logs docking output to flexx_docking.log.

Checkpoint: flexx_docking_done.chk.

**3. Step 3** – Filter Poses and Save CSV

Extracts individual _01 poses from the docked SDF.

Saves individual SDF files to docking_output_dir.

Extracts docking scores (BIOSOLVEIT.DOCKING_SCORE) and saves a CSV summary.

Checkpoints: filter_poses_vs_run.chk, csv_creation_vs_run.chk.


## Master Script

The pipeline is wrapped in a master script (vs_flexx_pipeline.py) that runs all three steps sequentially:

```bash
python vs_flexx_pipeline.py -c config.json
```

Runs Step 1 → Step 2 → Step 3 automatically.

Stops execution if any step fails.

Logs all progress to standard output and step-specific log files.

## Configuration

The pipeline is controlled by a single JSON configuration file. Example:

```bash
{
  "input_mae_dir": "mae",
  "output_base_dir": "vs_output",
  "output_sdf_dir": "vs_output/sdf",
  "merged_sdf_path": "vs_output/all_ligands.sdf",
  "checkpoint_dir": "checkpoints",
  "checkpoint_prefix": "vs_run",
  "input_sdf": "vs_output/all_ligands.sdf",
  "protein_path": "Pro_Ref_lig/pro.pdb",
  "reference_ligand": "Pro_Ref_lig/lig.sdf",
  "flexx_executable": "path/to/flexx_executable",
  "docking_output_sdf_name": "vs_run_flexx_docked.sdf",
  "docking_output_dir": "vs_output/docking_results"
}

```

Key Fields:

```bash
input_mae_dir: Directory containing original MAE ligand files.
output_base_dir: Base directory for all outputs of the pipeline.
output_sdf_dir: Directory for individual SDF ligands converted from MAE.
merged_sdf_path: Path to the merged SDF library for docking.
checkpoint_dir: Directory to store checkpoint files.
checkpoint_prefix: Prefix used for checkpoint files and outputs.
input_sdf: Path to the merged SDF library used for docking.
protein_path: Path to the prepared protein for docking.
reference_ligand: Path to the reference ligand for FlexX docking.
flexx_executable: Path to the FlexX binary executable.
docking_output_sdf_name: Filename for docked poses output from FlexX.
docking_output_dir: Directory to save filtered individual poses and CSV summary.

```

## Logging and Checkpoints

Each step maintains checkpoints to avoid recomputation:

Step 1: mae_to_sdf_vs_run.chk, merge_sdf_vs_run.chk
Step 2: flexx_docking_done.chk
Step 3: filter_poses_vs_run.chk, csv_creation_vs_run.chk

Step-specific logs (e.g., docking logs) are saved in output_base_dir.

## Running the Pipeline

1. Prepare the configuration file (config.json).

2. Ensure all directories exist or are correctly specified in the config.

3. Activate the environment:

```bash
conda activate vs-pipeline
```

4. Run the master script:

```bash
python vs_flexx_pipeline.py -c config.json
```

Monitor logs in the console or step-specific log files.

Checkpoints allow resuming if the process is interrupted.

## Notes

* MAE ligand files must be consistent with the pipeline input.

* The reference ligand should match the prepared protein target.

* Pipeline supports resumable execution for large-scale screening.

* Output SDF files and CSV results are ready for downstream analysis.