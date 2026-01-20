# Pipeline Overview

This directory provides a high-level overview of the modular virtual screening
workflow implemented in this repository. The pipeline is designed to support
lead compound discovery for arbitrary biological targets by combining data
curation, workflow optimization, retrospective validation, large-scale virtual
screening, and downstream structural analysis.

Detailed implementation instructions, configuration options, and executable
scripts are documented in the `README.md` files located within each pipeline
stage directory under `pipeline/`.


## Conceptual Design

The workflow is organized into sequential but modular stages. Each stage
addresses a distinct methodological goal and can be adapted or extended
independently depending on the target system and screening strategy.

At a high level, the pipeline proceeds from compound and bioactivity data
preparation, through workflow optimization and validation, to large-scale
virtual screening and downstream structural analysis. Both physics-based and
AI-driven approaches are supported where applicable.


## Pipeline Stages

### Stage 01 – CompoundUniqifier

This stage focuses on preparing compound datasets for downstream use by
ensuring consistency, uniqueness, and standardized representations. It serves
as the entry point for compound libraries intended for screening or model
development.

Implementation details are provided in:
`pipeline/01_CompoundUniqifier/README.md`


### Stage 02 – SARUniqifier

This stage refines compound datasets in the context of structure–activity
relationships by integrating and harmonizing bioactivity information from
multiple sources. The goal is to generate curated datasets suitable for
retrospective analysis and method evaluation.

Implementation details are provided in:
`pipeline/02_SARUniqifier/README.md`


### Stage 03 – Optimization

This stage evaluates and optimizes virtual screening workflows using both
physics-based docking methods and AI-driven approaches. Cross-docking and pose
comparison strategies are employed to assess robustness and reproducibility
across different tools and configurations.

Implementation details are provided in:
`pipeline/03_Optimization/README.md`


### Stage 04 – Validation

This stage performs retrospective validation of optimized workflows using
active and decoy sets. Scoring performance is assessed using statistical and
classification-based metrics to compare methods and parameterizations in a
target-specific context.

Implementation details are provided in:
`pipeline/04_Validation/README.md`


### Stage 05 – Virtual Screening

This stage applies selected workflows to large compound libraries for lead
identification. Screening is performed using scalable, batch-oriented pipelines
tailored to the selected docking or prediction method.

Implementation details are provided in:
`pipeline/05_Virtual_Screening/README.md`


### Stage 06 – Downstream Analysis

This stage contains post-screening utilities supporting structural analysis,
including preparation of protein–ligand complexes for comparative studies.
Co-folded structures are handled explicitly to enable consistent downstream
evaluation and comparison.

Implementation details are provided in:
`pipeline/06_Downstream/README.md`


## Scope and Intended Use

This overview is intended to describe the conceptual organization of the
workflow. Users are encouraged to consult the stage-specific documentation
for practical usage instructions, configuration examples, and executable
commands.
