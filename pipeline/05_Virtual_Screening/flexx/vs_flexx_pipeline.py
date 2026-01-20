import subprocess
import argparse
import json
import sys
from pathlib import Path

def run_step(script_name, config_path):
    print(f"\n=== Running {script_name} ===")
    try:
        result = subprocess.run(
            [sys.executable, script_name, "-c", config_path],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:\n{e.stderr}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Master pipeline runner for FlexX workflow")
    parser.add_argument("-c", "--config", required=True, help="Path to JSON config file")
    args = parser.parse_args()

    config_path = args.config

    with open(config_path) as f:
        config = json.load(f)

    step_scripts = config.get("step_scripts", {})
    if not step_scripts:
        print("Error: step_scripts not defined in config.")
        sys.exit(1)

    for step_name in ["step1", "step2", "step3"]:
        script_path = step_scripts.get(step_name)
        if not script_path or not Path(script_path).exists():
            print(f"Error: Script for {step_name} not found at {script_path}")
            sys.exit(1)
        run_step(script_path, config_path)

    print("\nAll pipeline steps completed successfully.")

if __name__ == "__main__":
    main()
