# Glide Virtual Screening Pipeline

This repository contains a fully automated Glide-based virtual screening pipeline designed to process large ligand libraries, generate docking input scripts, run parallel Glide docking, and process docking outputs. The pipeline supports checkpoints, batch processing, and structured logging.

## Overview

The Glide pipeline automates the following tasks:

MAE Preparation & Input Script Generation – Copies MAE files to a working directory and generates Glide .in scripts.

Batch Docking Submission – Submits .in scripts to Glide in parallel batches.

Docking Result Processing – Safely copies and decompresses .sdfgz outputs into .sdf files.

Checkpoints & Logging – Tracks progress and allows the pipeline to resume after interruptions.

This workflow is optimized for high-throughput virtual screening with large ligand libraries.

## Pipeline Workflow

The pipeline consists of three main steps:

**1. Step 1** – Prepare MAE Files and Generate Input Scripts

Copies ligands from mae_dir into a working directory (copied_mae_dir).

Generates Glide .in input scripts in input_scripts_dir.

.in scripts include docking parameters such as GRIDFILE, LIGANDFILE, DOCKING_METHOD, FORCEFIELD, and PRECISION.

Checkpoints: copy_mae_dir.chk, generated_in_files.chk.

**2. Step 2** – Submit Glide Docking Jobs

Reads .in scripts from input_scripts_dir.

Submits batches of Glide docking jobs (max_parallel controls batch size).

Tracks completed jobs in submitted_all_in_files.chk.

Can resume automatically for incomplete batches.

Uses ThreadPoolExecutor for parallel execution.

**3. Step 3** – Process Docking Results

Finds .sdfgz output files in output_files_dir.

Copies and decompresses them into .sdf format in docking_results_dir.

Generates checkpoint for failed or incomplete jobs: failed_jobs.chk.

Final checkpoint indicates that all processes are complete: all_process_done.chk.

## Master Script

The pipeline is wrapped in a master script (master_glide.py) that runs all three steps sequentially:

```bash
python master_glide.py config.json --max_parallel 24
```

Runs Step 1 → Step 2 → Step 3 automatically.

Stops execution if any step fails.

Logs all progress to logs/master.log.

## Configuration

The pipeline is controlled by a single JSON configuration file. Example:

```bash
{
  "mae_dir": "mae",
  "copied_mae_dir": "copied_mae",
  "checkpoints_dir": "checkpoints",
  "glide_path": "path/to/glide",
  "log_dir": "logs",
  "input_scripts_dir": "input_scripts",
  "grid_file": "grids/grid.zip",
  "docking_output_dir": "docking_results",
  "output_files_dir": "input_scripts",
  "checkpoint_file_name": "failed_jobs.chk",
  "docking_results_dir": "docking_results",
  "step_scripts": {
    "step1": "pipeline_step1.py",
    "step2": "pipeline_step2.py",
    "step3": "pipeline_step3.py"
  }
```

Key Fields:

```bash
mae_dir: Directory containing original MAE ligand files.
copied_mae_dir: Working copy of MAE files for processing.
checkpoints_dir: Directory to store checkpoint files.
glide_path: Path to the Glide executable.
log_dir: Directory for logs of all pipeline steps.
input_scripts_dir: Directory for generated .in input scripts (also used for output staging in step3).
grid_file: Glide grid file defining the docking site.
docking_output_dir: Directory to store raw docking outputs from Glide (.sdfgz files).
output_files_dir: Directory containing intermediate or raw Glide outputs (used for processing in step3).
checkpoint_file_name: Filename to track incomplete docking results.
docking_results_dir: Directory to store final decompressed docking results (.sdf).
step_scripts: Paths to the three pipeline step scripts:
  step1: pipeline_step1.py
  step2: pipeline_step2.py
  step3: pipeline_step3.py

```

## Logging and Checkpoints

Logs are written to logs/.

Each step maintains checkpoints to avoid recomputation.

  Step 1: copy_mae_dir.chk, generated_in_files.chk.

  Step 2: submitted_all_in_files.chk.

  Step 3: failed_jobs.chk, all_process_done.chk.

## Running the Pipeline

1. Prepare the configuration file (config.json).

2. Ensure all directories exist or are specified in the config.

3. Run the master script:

```bash
python master_glide.py config.json --max_parallel 24
```

Monitor logs in logs/.

Checkpoints allow resuming if the process is interrupted.

## Notes

* .mae ligand files must be consistent with the pipeline input.

* Grid files must correctly cover the binding site.

* Pipeline supports resumable execution for large-scale screening.

* Output .sdf files are ready for downstream analysis.
