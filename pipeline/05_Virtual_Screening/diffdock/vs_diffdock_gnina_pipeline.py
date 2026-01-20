#!/usr/bin/env python3
import os
import json
import shutil
import gzip
import logging
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess
import pandas as pd
import argparse


def setup_logger(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def copy_and_rename_sdf(results_dir, copied_dir, logger, copy_threads):
    os.makedirs(copied_dir, exist_ok=True)

    if not any(Path(results_dir).iterdir()):
        logger.error(f"Results directory is empty: {results_dir}")
        return []

    sdf_tasks = []

    for root, dirs, files in os.walk(results_dir):
        for d in dirs:
            rank1_path = Path(root) / d / "rank1.sdf"
            if rank1_path.exists():
                output_path = Path(copied_dir) / f"{d}.sdf"
                sdf_tasks.append((rank1_path, output_path))

    if not sdf_tasks:
        logger.info("No rank1.sdf files found.")
        return []

    def task(src_dst):
        src, dst = src_dst
        try:
            shutil.copy2(src, dst)
            logger.info(f"Copied {dst.name}")
            return dst
        except Exception as e:
            logger.error(f"Failed to copy {src} -> {dst}: {e}")
            return None

    with ThreadPoolExecutor(max_workers=min(len(sdf_tasks), copy_threads)) as executor:
        copied_files = list(filter(None, executor.map(task, sdf_tasks)))

    return copied_files


def gnina_rescore(copied_files, protein_file, rescored_dir, gnina_exec, logger):
    os.makedirs(rescored_dir, exist_ok=True)

    for sdf_file in copied_files:
        out_file = Path(rescored_dir) / f"{sdf_file.stem}_rescored.sdf.gz"
        cmd = [
            gnina_exec,
            "-r", protein_file,
            "-l", str(sdf_file),
            "--minimize",
            "--seed", "1",
            "-o", str(out_file)
        ]
        try:
            subprocess.run(cmd, check=True)
            logger.info(f"Rescored {sdf_file.name}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error rescoring {sdf_file}: {e}")


def read_sdf_file(path: Path) -> str:
    try:
        if str(path).endswith(".gz"):
            with gzip.open(path, "rt") as f:
                return f.read()
        else:
            with open(path, "r") as f:
                return f.read()
    except Exception:
        return ""


def extract_metrics_to_csv(sdf_folder: Path, csv_out: Path, logger: logging.Logger):
    patterns = {
        "minimizedAffinity": r"> <minimizedAffinity>\n(.*?)\n",
        "CNNscore": r"> <CNNscore>\n(.*?)\n",
        "CNNaffinity": r"> <CNNaffinity>\n(.*?)\n",
        "CNN_VS": r"> <CNN_VS>\n(.*?)\n",
        "CNNaffinity_variance": r"> <CNNaffinity_variance>\n(.*?)\n",
    }

    data = []

    for file in Path(sdf_folder).glob("*"):
        if file.suffix in [".sdf", ".gz"]:
            content = read_sdf_file(file)
            if not content:
                continue
            row = {"File": file.name}
            for key, pattern in patterns.items():
                match = re.search(pattern, content)
                row[key] = match.group(1) if match else None
            data.append(row)

    if data:
        pd.DataFrame(data).to_csv(csv_out, index=False)
        logger.info(f"Saved CSV: {csv_out}")


def main():
    parser = argparse.ArgumentParser(description="GNINA rescoring pipeline")
    parser.add_argument("-c", "--config", required=True, help="Path to config JSON")
    args = parser.parse_args()

    with open(args.config) as f:
        cfg = json.load(f)

    chk_dir = Path(cfg["chk_dir"])
    chk_dir.mkdir(parents=True, exist_ok=True)

    log_file = chk_dir.parent / "gnina_pipeline.log"
    logger = setup_logger(log_file)

    copy_threads = cfg.get("parallel", 1)

    copied_chk = chk_dir / "copied.chk"
    if copied_chk.exists():
        copied_files = list(Path(cfg["copied_dir"]).glob("*.sdf"))
    else:
        copied_files = copy_and_rename_sdf(
            cfg["results_dir"],
            cfg["copied_dir"],
            logger,
            copy_threads
        )
        if not copied_files:
            return
        copied_chk.write_text("DONE")

    rescored_chk = chk_dir / "rescored.chk"
    if not rescored_chk.exists():
        gnina_rescore(
            copied_files,
            cfg["protein_file"],
            cfg["rescored_dir"],
            cfg["gnina_executable"],
            logger
        )
        rescored_chk.write_text("DONE")

    metrics_chk = chk_dir / "metrics.chk"
    if not metrics_chk.exists():
        csv_out = chk_dir.parent / f"gnina_score_{Path(cfg['results_dir']).name}.csv"
        extract_metrics_to_csv(cfg["rescored_dir"], csv_out, logger)
        metrics_chk.write_text("DONE")


if __name__ == "__main__":
    main()
