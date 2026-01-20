# Environment Setup for vs-pipeline

## 1. Create the Conda Environment

This project uses a Conda environment to manage Python dependencies.

```bash
conda env create -f environment.yml
conda activate vs-pipeline
```

This installs all required scientific, cheminformatics, and visualization libraries.

## 2. Optional External Tools

Some workflows rely on additional software not included in the environment:

- [**AutoDock Vina**] (https://vina.scripps.edu)  
- [**FlexX (BioSolveIT)**](https://www.biosolveit.de/download/), requires a valid license
- [**DiffDock**](https://github.com/gcorso/DiffDock)  
- [**Schrödinger**](https://www.schrodinger.com), requires a valid license  
- [**DEEPScreen2**](https://github.com/HUBioDataLab/DEEPScreen2) 
- [**GNINA**](https://github.com/gnina/gnina)

To make them discoverable:  
- Place executables on your `PATH`  
- Or set the appropriate environment variable (e.g., `SCHRODINGER`, `DEEPSCREEN_HOME`)


## Verify the Environment

After activating the environment, you can optionally check that everything is correctly installed:

```bash
python check_environment.py
```