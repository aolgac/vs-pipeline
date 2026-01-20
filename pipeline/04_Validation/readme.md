# 02_Validation Pipeline Overview

Purpose: Evaluate docking pipelines (Vina, Glide, FlexX, DiffDock, GNINA) by docking active ligands and decoys against a chosen receptor PDB. Then, extract results and compute ROC curves to quantify enrichment.

## 1 Prepare Receptor & Ligands

Inputs:

* Receptor: single PDB file of the target.

* Ligands:

        Actives (bioactive compounds for the target)

        Decoys (chemically similar compounds expected to be inactive)

Notes:

Ligand preparation may require conversion (.mae → .pdbqt for Vina, Glide prep, etc.).

Keep actives and decoys in separate folders (actives/, decoys/) for clarity.

## 2 Docking

Docking is performed using scripts from 01_Optimization. These can be reused directly for each docking engine.

        - Input: prepared receptor and ligand sets

        - Output: docking results stored in docking_results/ within each program folder

Notes:

* DiffDock poses do not have scores. Use 2_diffdock_score_w_gnina.py to score with GNINA.

* Adjust docking parameters using the corresponding .conf files if needed.

## 3 Score Extraction 

Each docking program has a script to extract scores into CSV files. Use the corresponding config files for paths and parameters.

After docking, extract the docking scores from each program into CSV files for downstream ROC analysis. Keep the output consistent with the table below:

| Program  | Script Name                                                 | Input Folder                     | Output CSV                                                                 | Conf File                      |
| -------- | ----------------------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------- | ------------------------------ |
| Vina     | `2_vina_extract_scores.py`                                  | `actives/` and `decoys/` folders | `vina_results_actives.csv` / `vina_results_decoys.csv`                     | `vina_scores.conf.example`     |
| Glide    | `2_glide_extract_scores.py`                                 | `actives/` and `decoys/` folders | `glide_results_actives.csv` / `glide_results_decoys.csv`                   | `glide_scores.conf.example`    |
| FlexX    | `2_flexx_extract_scores.py`                                 | `actives/` and `decoys/` folders | `flexx_results_actives.csv` / `flexx_results_decoys.csv`                   | `flexx_scores.conf.example`    |
| GNINA    | `2_gnina_extract_scores.py`                                 | `actives/` and `decoys/` folders | `gnina_results_actives.csv` / `gnina_results_decoys.csv`                   | `gnina_scores.conf.example`    |
| DiffDock | `2_diffdock_extract_scores.py` (after rescoring with GNINA) | `actives/` and `decoys/` folders | `diffdock_gnina_results_actives.csv` / `diffdock_gnina_results_decoys.csv` | `diffdock_scores.conf.example` |


Tips:

* Keep actives and decoys in separate folders.

* All scripts that extract scores read directly from the docking results folder.

* Make sure .conf files point to the correct directories and filenames above.

## 4 Plot ROC Curves

Once scores are extracted, compute ROC curves to quantify enrichment of actives over decoys. Use the same filenames for inputs as above.

| Program  | Script Name              | Input Actives CSV                    | Input Decoys CSV                    | Output Figure                      | Conf File                   |
| -------- | ------------------------ | ------------------------------------ | ----------------------------------- | ---------------------------------- | --------------------------- |
| Vina     | `3_vina_plot_roc.py`     | `vina_results_actives.csv`           | `vina_results_decoys.csv`           | `ROC_Curve_AUC_vina.png`           | `vina_roc.conf.example`     |
| Glide    | `3_glide_plot_roc.py`    | `glide_results_actives.csv`          | `glide_results_decoys.csv`          | `ROC_Curve_AUC_glide.png`          | `glide_roc.conf.example`    |
| FlexX    | `3_flexx_plot_roc.py`    | `flexx_results_actives.csv`          | `flexx_results_decoys.csv`          | `ROC_Curve_AUC_flexx.png`          | `flexx_roc.conf.example`    |
| GNINA    | `3_gnina_plot_roc.py`    | `gnina_results_actives.csv`          | `gnina_results_decoys.csv`          | `ROC_Curve_AUC_gnina.png`          | `gnina_roc.conf.example`    |
| DiffDock | `3_diffdock_plot_roc.py` | `diffdock_gnina_results_actives.csv` | `diffdock_gnina_results_decoys.csv` | `ROC_Curve_AUC_diffdock_gnina.png` | `diffdock_roc.conf.example` |


Notes:
* Update the .conf files (*_roc.conf.example) with the correct paths for actives_file, decoys_file, and save_path.
* Keep consistent file naming between score extraction and ROC plotting to avoid errors.