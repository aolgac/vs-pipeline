import subprocess
import logging
import time
from pathlib import Path
from multiprocessing import Pool, cpu_count
import sys

def load_config(cfg_path):
    cfg = {}
    with open(cfg_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip()
    return cfg

def convert_mae_to_mol2(args):
    mae_file, schrodinger_run, mol2_dir = args
    mol2_file = mol2_dir / (mae_file.stem + ".mol2")
    cmd = [schrodinger_run, "structconvert.py", str(mae_file), str(mol2_file)]
    subprocess.run(cmd, check=True)
    logging.info(f"MAE→MOL2: {mae_file.name}")

def convert_mol2_to_pdbqt(args):
    mol2_file, pythonsh, prepare_script, pdbqt_dir = args
    pdbqt_file = pdbqt_dir / (mol2_file.stem + ".pdbqt")
    cmd = [pythonsh, prepare_script, "-l", str(mol2_file), "-o", str(pdbqt_file)]
    subprocess.run(cmd, check=True)
    logging.info(f"MOL2→PDBQT: {mol2_file.name}")

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python convert_ligands_mae_to_pdbqt.py config.conf")

    cfg = load_config(sys.argv[1])

    logging.basicConfig(
        filename=cfg.get("LOG_FILE", "ligand_conversion.log"),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

    ligands_dir = Path(cfg["LIGANDS_DIR"])
    mol2_dir = Path(cfg["MOL2_OUTPUT_DIR"])
    pdbqt_dir = Path(cfg["PDBQT_OUTPUT_DIR"])
    mol2_dir.mkdir(exist_ok=True)
    pdbqt_dir.mkdir(exist_ok=True)

    mae_files = list(ligands_dir.glob("*.mae"))

    start = time.time()

    with Pool(min(cpu_count(), int(cfg.get("N_PROCS", 8)))) as pool:
        pool.map(
            convert_mae_to_mol2,
            [(f, cfg["SCHRODINGER_RUN"], mol2_dir) for f in mae_files]
        )

    mol2_files = list(mol2_dir.glob("*.mol2"))

    with Pool(min(cpu_count(), int(cfg.get("N_PROCS", 8)))) as pool:
        pool.map(
            convert_mol2_to_pdbqt,
            [(f, cfg["MGLTOOLS_PYTHONSH"], cfg["PREPARE_LIGAND_SCRIPT"], pdbqt_dir)
             for f in mol2_files]
        )

    logging.info(f"Completed in {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    main()
