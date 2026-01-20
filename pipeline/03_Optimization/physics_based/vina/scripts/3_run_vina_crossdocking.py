import subprocess
import logging
from multiprocessing import Pool
from pathlib import Path
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

def run_docking(args):
    protein, ligand, cfg = args

    out_file = cfg["OUTPUT_DIR"] / f"{protein.stem}_{ligand.stem}.pdbqt"

    cmd = [
        cfg["VINA_BINARY"],
        "--receptor", str(protein),
        "--ligand", str(ligand),
        "--config", cfg["VINA_CONFIG"],
        "--cpu", "1",
        "--seed", "1",
        "--out", str(out_file)
    ]

    logging.info(f"Docking {protein.name} vs {ligand.name}")
    res = subprocess.run(cmd, capture_output=True, text=True)

    if res.stderr:
        logging.error(res.stderr)

    if not out_file.exists():
        logging.error(f"Missing output: {out_file.name}")

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python run_vina_crossdocking.py config.conf")

    cfg_raw = load_config(sys.argv[1])

    cfg = {
        "PROTEIN_DIR": Path(cfg_raw["PROTEIN_DIR"]),
        "LIGAND_DIR": Path(cfg_raw["LIGAND_DIR"]),
        "OUTPUT_DIR": Path(cfg_raw["OUTPUT_DIR"]),
        "VINA_BINARY": cfg_raw["VINA_BINARY"],
        "VINA_CONFIG": cfg_raw["VINA_CONFIG"],
        "N_PROCS": int(cfg_raw.get("N_PROCS", 8)),
    }

    cfg["OUTPUT_DIR"].mkdir(exist_ok=True)

    logging.basicConfig(
        filename=cfg_raw.get("LOG_FILE", "vina_crossdocking.log"),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
    )

    proteins = list(cfg["PROTEIN_DIR"].glob("*.pdbqt"))
    ligands = list(cfg["LIGAND_DIR"].glob("*.pdbqt"))

    jobs = [(p, l, cfg) for p in proteins for l in ligands]

    with Pool(cfg["N_PROCS"]) as pool:
        pool.map(run_docking, jobs)

if __name__ == "__main__":
    main()
