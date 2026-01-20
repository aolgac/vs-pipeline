# DiffDock Virtual Screening Pipeline

This repository contains a fully automated DiffDock-based virtual screening pipeline designed to process ligands selected from a prior machine-learning screen, convert them into DiffDock-compatible formats, generate protein–ligand pairing inputs, and prepare GPU-based DiffDock inference jobs.
The pipeline supports checkpoints, parallel preprocessing, optional SLURM integration, and downstream GNINA rescoring.

Ligand selection prior to DiffDock is performed using DeepScreen2, which is used to create a CSV of predicted active compounds. That CSV is treated as an external input to this pipeline.

## Overview

The DiffDock pipeline automates the following tasks:

Ligand Selection (External) – Uses DeepScreen2 predictions to define a filtered ligand list in CSV format.

Ligand Extraction – Extracts selected ligands from large .mae files based on the DeepScreen2 CSV.

Format Conversion – Converts extracted ligands from .mae to .mol2 format.

DiffDock Input Generation – Builds a protein–ligand pairing CSV required for DiffDock inference.

SLURM Script Generation – Creates GPU job scripts for DiffDock without automatic submission.

Batch Job Submission (Optional) – Submits and monitors multiple DiffDock jobs sequentially on HPC systems.

Post-Docking Rescoring – Scores DiffDock poses using GNINA and extracts CNN-based scoring metrics.

This workflow is optimized for GPU-accelerated structure-based virtual screening with ML-guided ligand filtering.

## Pipeline Workflow

The pipeline consists of six main stages:

1. Ligand Selection via DeepScreen2 (External)

Ligands are first screened using DeepScreen2.

The output is a CSV file containing predicted ligands of interest.

This pipeline assumes the CSV already exists and does not perform DeepScreen2 inference internally.

Required column:
Molecule Name

2. Ligand Extraction from MAE Files

Parses .mae files and extracts ligands listed in the DeepScreen2 CSV.

Each ligand is written as an individual .mae file.

Naming convention:
<vs_context>_<ligand_name>.mae

Extraction is checkpointed per ligand to allow resumable execution.

Checkpoints:
<ligand_name>.mae.chk

3. MAE → MOL2 Conversion

Converts extracted .mae files to .mol2 using Schrödinger structconvert.py.

Conversion is parallelized using ThreadPoolExecutor.

Each successful conversion creates a checkpoint file.

Checkpoints:
<ligand_name>.mol2.chk

4. DiffDock Input CSV Generation

Scans the ligand directory for .mol2 (or .sdf) files.

Generates a CSV file required by DiffDock inference containing:

complex_name

protein_path

ligand_description

protein_sequence (optional, left empty)

This CSV serves as the single input file for DiffDock inference.

5. SLURM Script Generation and Execution (Optional)

Generates a GPU SLURM job script for DiffDock inference.

The script:

Activates the DiffDock environment

Runs DiffDock inference using the generated CSV

Writes outputs to a defined directory

Job submission is intentionally separated from script generation.

An optional batch submission script supports:

Sequential job submission

Job monitoring

Safe execution for large ligand libraries split across multiple configs

6. GNINA Rescoring

After DiffDock inference, top-ranked poses (rank1.sdf) can be rescored using GNINA.

The GNINA pipeline performs:

Copying and renaming DiffDock rank1 poses

GPU-based GNINA rescoring with minimization

Extraction of CNN-based metrics into a CSV

Extracted metrics include:

* minimizedAffinity

* CNNscore

* CNNaffinity

* CNN_VS

* CNNaffinity_variance

Stage-level checkpoints allow each rescoring step to be resumed safely.

## Configuration

The preprocessing and DiffDock stages are controlled by a JSON configuration file. Example:

```bash
{
  "mae_dir": "mae",
  "csv_file": "ligand_list.csv",
  "extracted_mae_dir": "work/extracted_mae",
  "mol2_output_dir": "work/mol2",
  "checkpoint_dir": "checkpoints",
  "log_dir": "logs",
  "protein_file": "protein/protein.pdb",
  "final_csv_output": "diffdock_inputs.csv",
  "slurm_dir": "slurm",
  "slurm_output_dir": "diffdock_outputs",
  "slurm_script_name": "diffdock_job.sh"
}

```

GNINA rescoring is controlled by a separate JSON configuration file and is executed after DiffDock inference has completed.

```bash
{
  "results_dir": "diffdock_outputs",
  "copied_dir": "gnina/work/copied",
  "rescored_dir": "gnina/work/rescored",
  "chk_dir": "gnina/checkpoints",
  "protein_file": "protein/protein.pdb",
  "parallel": 24
}

```

Key fields:

Diffdock:

```bash
mae_dir: Directory containing source MAE ligand files.
csv_file: CSV listing ligand names to extract (column: Molecule Name).
extracted_mae_dir: Output directory for extracted MAE ligands.
mol2_output_dir: Output directory for converted MOL2 ligands.
checkpoint_dir: Directory storing pipeline checkpoint files.
log_dir: Directory for pipeline logs.
protein_file: Protein structure used for all DiffDock complexes.
final_csv_output: CSV input file consumed by DiffDock inference.
slurm_dir: Directory where SLURM scripts are generated.
slurm_output_dir: Directory where DiffDock outputs are written.
slurm_script_name: Filename of the generated SLURM script.

```

GNINA:

```bash
results_dir:
Directory containing DiffDock output folders.
Each subdirectory is expected to contain a rank1.sdf file.

copied_dir:
Working directory where rank1.sdf files are copied and renamed
to a flat structure prior to rescoring.

rescored_dir:
Output directory for GNINA-rescored SDF files
(typically written as .sdf.gz).

chk_dir:
Directory for GNINA stage-level checkpoint files
(copy, rescore, metrics).

protein_file:
Protein structure used for GNINA rescoring.
Must match the protein used in DiffDock.

parallel:
Maximum number of parallel file copy operations.
GNINA rescoring itself is executed sequentially per ligand.
```

## Running the Pipeline

1. Prepare DeepScreen2 predictions

Run DeepScreen2 externally and generate a ligand CSV.

2. Prepare the DiffDock configuration file

Edit vs_diffdock_config.json to reflect your directory structure.

3. Run the preprocessing pipeline

```bash
python vs_diffdock_pipeline.py --config vs_diffdock_config.json
```
This performs:

* Ligand extraction

* MAE → MOL2 conversion

* DiffDock CSV generation

* SLURM script creation

4.  Submit the DiffDock SLURM job (optional)

```bash
sbatch slurm/diffdock_job.sh
```
5. Batch execution (optional)

For large screens split across multiple configs:

```bash
python submit_diffdock_batches.py
```

6. GNINA rescoring

```bash
python vs_diffdock_gnina_pipeline.py --config vs_diffdock_gnina_config.json
```

## Logging and Checkpoints

Logs are written to:

```bash
logs/pipeline.log
submission_log.log
gnina_pipeline.log

```
Checkpoints allow safe resumption of interrupted runs:

  * Ligand extraction checkpoints

  * Conversion checkpoints

  * DiffDock batch submission tracking

  * GNINA stage-level checkpoints

## Notes

  * DeepScreen2 prediction is an external prerequisite and is not executed within this repository.

  * The pipeline does not submit SLURM jobs automatically unless explicitly requested.

  * DiffDock inference parameters are defined in the SLURM script, not the JSON config.

  * Protein preparation must be completed prior to running the pipeline.

  * DiffDock outputs are directly compatible with the GNINA rescoring pipeline and downstream analysis workflows..