# 01_Optimization

This directory contains all optimization pipelines for protein-ligand docking, including **physics-based** and **AI-driven** approaches. Each pipeline has its own scripts, configuration files, and sequential steps for running cross-docking, RMSD calculations, and result visualization.

## Environment

Activate the global Conda environment before running any scripts:

```bash
conda activate vs-pipeline
```

Ensure all .conf files are correctly set to point to input/output directories before running the pipelines.

## Directory Structure

03_Optimization/

├── ai_driven/

│   ├── diffdock/

│   └── gnina/

├── physics_based/

│   ├── flexx/

│   ├── glide/

│   └── vina/

└── README.md


* ai_driven/: Contains pipelines that use AI or ML models for docking and pose prediction.

    diffdock/: DiffDock cross-docking pipeline.

    gnina/: GNINA cross-docking pipeline.

* physics_based/: Contains classical physics-based docking pipelines.

    flexx/: FlexX docking pipeline.

    glide/: Glide docking pipeline.

    vina/: Vina docking pipeline.

Each subfolder contains numbered scripts (1_..., 2_..., etc.) and corresponding .conf files that define parameters, input/output paths, and other settings.

## General Usage

Each pipeline can be executed step by step using its wrapper script (if available) or manually by running the numbered scripts in order:

```bash
python run_<pipeline>_pipeline.py
```

For example:

```bash
cd ai_driven/gnina
python run_gnina_pipeline.py
```

* Wrapper scripts automatically execute all steps in sequence, using their respective configuration files.

* Manual execution is possible by running the numbered scripts in order: 1 → 2 → 3 → … → N.

## Output

* Docked ligand poses (.sdf or .pdbqt)

* RMSD calculations (.csv)

* RMSD matrices (.csv)

* Heatmaps and figures (.png)

Outputs are generally stored in pipeline-specific folders defined in the .conf files.

## Notes

* Ensure all input ligand and receptor files are correctly prepared before running the pipelines.

* HPC usage or parallelization may be required for large datasets.

* Each sub-pipeline (AI-based or physics-based) has its own README for detailed step-by-step instructions.