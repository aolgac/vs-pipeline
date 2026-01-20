#!/usr/bin/env python3

import sys
import os
import shutil


def check_import(name):
    try:
        __import__(name)
        print(f"[OK] Python module: {name}")
        return True
    except ImportError:
        print(f"[NOT DETECTED] Python module: {name}")
        return False


def check_binary(name):
    if shutil.which(name):
        print(f"[OK] {name}")
        return True
    else:
        print(f"[NOT DETECTED] {name}")
        return False


def check_env_var(var, label):
    path = os.environ.get(var)
    if path and os.path.isdir(path):
        print(f"[OK] {label}")
        return True
    else:
        print(f"[NOT DETECTED] {label}")
        return False


def check_deepscreen():
    try:
        __import__("deepscreen")
        print("[OK] DEEPScreen2")
        return True
    except ImportError:
        return check_env_var("DEEPSCREEN_HOME", "DEEPScreen2")


def main():
    print(f"Python version: {sys.version.split()[0]}\n")

    ok = True

    # Core Python dependencies
    ok &= check_import("numpy")
    ok &= check_import("pandas")
    ok &= check_import("scipy")
    ok &= check_import("Bio")
    ok &= check_import("rdkit")
    ok &= check_import("sklearn")
    ok &= check_import("yaml")
    ok &= check_import("matplotlib")
    ok &= check_import("seaborn")

    # Optional Python tools (reported, not enforced)
    check_import("pymol")
    check_import("posebusters")

    print("\n--- External dependencies ---")
    check_binary("vina")
    check_binary("flexx")
    check_binary("diffdock")
    check_env_var("SCHRODINGER", "Schrödinger suite")
    check_deepscreen()

    print("\n--- Summary ---")
    if ok:
        print("Core environment OK")
    else:
        print("Core environment incomplete")
        sys.exit(1)


if __name__ == "__main__":
    main()
