# Virtual Screening Pipelines

This directory contains multiple structure-based virtual screening pipelines implemented using different docking engines.
Each subdirectory is self-contained and includes its own scripts, configuration files, and documentation.

## Directory Structure

```bash
05_Virtual_Screening

├── diffdock
│   ├── readme.md
│   ├── submit_diffdock_batches.py
│   ├── vs_diffdock_config.json
│   ├── vs_diffdock_gnina_config.json
│   ├── vs_diffdock_gnina_pipeline.py
│   └── vs_diffdock_pipeline.py
├── flexx
│   ├── pipeline_step1.py
│   ├── pipeline_step2.py
│   ├── pipeline_step3.py
│   ├── readme.md
│   ├── vs_flexx_config.json
│   └── vs_flexx_pipeline.py
├── glide
│   ├── pipeline_step1.py
│   ├── pipeline_step2.py
│   ├── pipeline_step3.py
│   ├── readme.md
│   ├── vs_glide_config.json
│   └── vs_glide_pipeline.py
└── vina
    ├── readme.md
    ├── vs_vina_config.json
    └── vs_vina_pipeline.py
```

## Notes

 - Pipelines are independent and can be used separately.

 - All paths, parameters, and execution settings are defined via JSON configuration files.

 - Detailed documentation is provided within each subdirectory